import re
import unicodedata
import json 
import pandas as pd
import re, sys, json, os 
import re
import unicodedata
import re, sys, json, os 
import re
import unicodedata
from preprocess.numeric_case import *
import difflib

def compare_string(result, cleaned_choices):
    close_matches = difflib.get_close_matches(str(result), 
                cleaned_choices, 1, 0)[0]
    return  cleaned_choices.index(close_matches)

def rule_based_numeric_math(question, choices):
    if case1(question, choices)!=[]:
        answer = case1(question, choices)
    elif case2(question, choices)!=[]:
        answer = case1(question, choices)
    elif case3(question, choices)!=[]:
        answer = case3(question, choices)
    elif case4(question, choices)!=[]:
        answer = case4(question, choices)
    elif case5(question, choices)!=[]:
        answer = case5(question, choices)    
    elif case6(question, choices)!=[]:
        answer = case6(question, choices)
    elif case7(question, choices)!=[]:
        answer = case7(question, choices)
    elif case8(question, choices)!=[]:
        answer = case8(question, choices) 
    elif case9(question, choices)!=[]:
        answer = case9(question, choices)
    else:
        return False, None 
    if len(answer) == 0:
        return False, []
    if answer not in choices:
        if isinstance(answer, list):
            answer_str = str(answer[0])
            for item in answer[1:]:
                answer_str += ", " + str(item)
            
            selected_idx = compare_string(answer_str, choices)
        else:
            selected_idx = compare_string(str(answer), choices)
        answer  = choices[selected_idx]
    return True, answer

def process_numeric_math(item):
    status, answer = rule_based_numeric_math(item["question"], item["choices"])
    return status, answer

if __name__ == "__main__":
    file_test = open("/hdd4/duongnh/project/ZaloAIChallenge/zalo_ai_2023_elementary_maths_solving/math_train.json", 'r')
    data_test = json.load(file_test)["data"]
    count = 0
    l_used_id = []
    path_src_submit_df = "/hdd4/duongnh/project/ZaloAIChallenge/output_submit/submission_qwen_14b_best_28_11.csv"
    df_src = pd.read_csv(path_src_submit_df)
    l_ids = df_src["id"].tolist()
    l_answer = df_src["answer"].tolist()
    count = 0
    for idx, item in enumerate(data_test):
        status, answer = process_numeric_math(item["question"], item["choices"])
        if status and len(answer) != 0:
            count += 1
            if answer != item["answer"]:
                print("Question: ", item["question"])
                print("Choices: ", item["choices"])
                print("Labels: ", item["answer"])
                print("answer: ", answer)
                print("$#############")
            # l_used_id.append(idx)
            # l_answer[idx] = answer
            # print("After: ", l_answer[idx])
            # print("############")
            # count += 1 
    print(count)
    
    # with open("/hdd4/duongnh/project/ZaloAIChallenge/temp/ignore_id.txt", 'w') as file:
    #     for idx in l_used_id:
    #         file.write(str(idx) + "\n")
    # file.close()

    # df_out = pd.DataFrame()
    # df_out["id"] = l_ids
    # df_out["answer"] = l_answer
    # df_out.to_csv("/hdd4/duongnh/project/ZaloAIChallenge/output_submit/submission_qwen_14b_best_28_11_update_v1.csv", index = False)
            