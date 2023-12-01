import numpy as np
import faiss
import json 
import os
import time 
import torch
from tqdm import tqdm
from faiss import write_index, read_index
from pyvi.ViTokenizer import tokenize
from sentence_transformers import SentenceTransformer
import difflib
from rank_bm25 import BM25Okapi
from preprocess.vietnamese_preprocess import tien_xu_li


def init_bm25(data):
    l_data_with_explanation = []
    l_tokens = []
    for item in data:
        if "explanation" in item:
            l_data_with_explanation.append(item)
            normalize_question = tien_xu_li(item["question"])
            l_tokens.append(normalize_question.split(" "))
    bm25 = BM25Okapi(l_tokens) 
    return bm25, l_data_with_explanation

def compare_string(result, cleaned_choices):
    close_matches = difflib.get_close_matches(str(result), 
                cleaned_choices, 1, 0)[0]
    return  cleaned_choices.index(close_matches)

# def generate_prompt_based_on_train(current_question, choices_str, search_faiss, model_embedding,\
#                                     prefix_prompt,data_train, num_selected = 20):
#     #Searching
#     sentences = [tokenize(current_question)]
#     embedding =  model_embedding.encode(sentences, show_progress_bar = False, device = torch.device("cpu"))
#     embedding = np.array(embedding).astype('float32')
#     f_dists, f_ids = search_faiss.search(embedding.reshape(1, -1), k=num_selected)
#     f_ids = f_ids[0]
#     prompt = prefix_prompt
#     num_used = 2
#     for idx in f_ids:
#         #select question in training csv 
#         selected_question = data_train[idx]["question"].replace("\n", "").replace("\t", "")
#         selected_choices = "\n".join(data_train[idx]["choices"])
#         selected_correct_answer = data_train[idx]["answer"]
#         if "explanation" in data_train[idx]:
#             if num_used == 0:
#                 break
#             selected_explanation = data_train[idx]["explanation"].replace("\n", "").replace("\t", "")
#             prompt += "\n\n" + "Question:\n" + selected_question + "\nOptions:\n" +\
#                     selected_choices + "\n" + "Solution: " +  selected_explanation +\
#                     "Options:\n"+ "Correct answer: " + selected_correct_answer
#             num_used -= 1
#         else:
#             continue
#     prompt += "\n\n" + "Question:\n" + current_question +\
#               "\nOptions:\n" +choices_str + "\nSolution:"
#     return prompt

def generate_prompt_based_on_train(current_question, choices_str, search_faiss,\
    model_embedding, prefix_prompt,data_train, num_selected = 20):
    #Searching
    sentences = [tokenize(current_question)]
    embedding =  model_embedding.encode(sentences, show_progress_bar = False)
    embedding = np.array(embedding).astype('float32')
    f_dists, f_ids = search_faiss.search(embedding.reshape(1, -1), k=num_selected)
    f_ids = f_ids[0]
    prompt = prefix_prompt
    num_used = 2
    for idx in f_ids:
        #select question in training csv 
        selected_question = data_train[idx]["question"].replace("\n", "").replace("\t", "")
        selected_choices = "\n".join(data_train[idx]["choices"])
        selected_correct_answer = data_train[idx]["answer"]
        if "explanation" in data_train[idx]:
            if num_used == 0:
                break
            selected_explanation = data_train[idx]["explanation"].replace("\n", "").replace("\t", "")
            prompt += "\n\n" + "Câu hỏi: " + selected_question + "\n" +\
                    selected_choices + "\n" + "Solution: " +  selected_explanation\
                    + "\n" + "Correct answer: " + selected_correct_answer
            num_used -= 1
        else:
            continue
    prompt += "\n\n" + "Câu hỏi: " + current_question + "\n" +\
              choices_str + "\nSolution:"
    return prompt

def generate_prompt_based_on_train_bm25(current_question, choices_str, bm25,\
    prefix_prompt,l_data_with_explanation, num_used = 2):
    #Searching
    sentences = tien_xu_li(current_question)
    tokenized_query = sentences.split(" ")
    l_selected_data = bm25.get_top_n(tokenized_query, l_data_with_explanation, n=num_used)
    prompt = prefix_prompt
    for selected_data in l_selected_data:
        selected_question = selected_data["question"].replace("\n", "").replace("\t", "")
        selected_choices = "\n".join(selected_data["choices"])
        selected_correct_answer = selected_data["answer"]
        selected_explanation = selected_data["explanation"].replace("\n", "").replace("\t", "")
        prompt += "\n\n" + "Câu hỏi: " + selected_question + "\n" +\
                selected_choices + "\n" + "Solution: " +  selected_explanation\
                + "\n" + "Correct answer: " + selected_correct_answer
    prompt += "\n\n" + "Câu hỏi: " + current_question + "\n" +\
              choices_str + "\nSolution: "
    return prompt

# def generate_prompt_no_search(current_question, choices_str,
#     prefix_prompt):
#     #Searching
#     prompt += "\n\n" + "Câu hỏi: " + current_question + "\n" +\
#               choices_str + "\nSolution: "
#     return prompt

def get_question_choices_prompt(item):
    question = item["question"]
    question = question.replace("\n", "").replace("\t", "")
    if question[-1] == ":":
        question = question[:-1] + "?"
    else:
        question = question + "?"
    choices = item["choices"]
    cleaned_choices = []
    for choice in choices: 
        if choice != None and len(choice) != 0:
            cleaned_choices.append(choice)
    choices_str = "\n".join(cleaned_choices)
    # question_choices_prompt = "Question:\n" + question + "\n" +\
    #           "Options:\n" + choices_str + "\nSolution: "
    question_choices_prompt = "Câu hỏi: " + question + "\n" +\
              choices_str + "\nSolution:"
    return question_choices_prompt, cleaned_choices

def get_answer_without_ABCD(tmp_output, cleaned_choices):
    tmp_output = tmp_output.replace("\n", "")
    for choice in cleaned_choices:
        if choice in tmp_output:
            answer = choice
            return answer
    idx_answer = compare_string(tmp_output[:20], cleaned_choices)
    answer = cleaned_choices[idx_answer]
    return answer
    

def get_final_choices(item_input, output_responce):
    question_choices_prompt, cleaned_choices = get_question_choices_prompt(item_input)
    start_idx = output_responce.index(question_choices_prompt) + len(question_choices_prompt)
    tmp_output = output_responce[start_idx:]
    tmp_search_str = ""
    if "Correct answer:" in tmp_output:
        tmp_search_str = "Correct answer:"
        
    elif "Answer:" in tmp_output:
        tmp_search_str = "Answer:"
        
    elif "Đáp án:" in tmp_output:
        tmp_search_str = "Đáp án:"
        
    elif "Kết quả:" in tmp_output:
        tmp_search_str = "Đáp án:"
        
    if tmp_search_str != "":
        start_answer_idx = tmp_output.index(tmp_search_str) + len(tmp_search_str)
        tmp_output = tmp_output[start_answer_idx:]
        if "\n" in tmp_output:
            end_idx = tmp_output.index("\n")
            tmp_output = tmp_output[:end_idx]
    tmp_output = tmp_output.replace("\n", " ").strip()
    type_answer = ['A.', 'B.', 'C.', 'D.']
    if tmp_output[:2] in type_answer:
        idx_answer = type_answer.index(tmp_output[:2])
        if idx_answer < len(cleaned_choices):
            answer = cleaned_choices[idx_answer]
        else:
            # answer = data_zalo_vn[idx]["choices"][0]
            print("Over choice")
            idx_answer = compare_string(tmp_output[:20], cleaned_choices)
            answer = cleaned_choices[idx_answer]
    else:
        print("Only selected A")
        print("Question: ", item_input["question"])
        print("Output: ", tmp_output.replace("\n", ""))
        print("#############")
        answer = get_answer_without_ABCD(tmp_output, cleaned_choices)
    return answer
    