import numpy as np
import faiss
import json 
import os
import time 
import torch
from tqdm import tqdm
from faiss import write_index, read_index
from pyvi.ViTokenizer import tokenize
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import os
import pandas as pd
from utils import generate_prompt_based_on_train, get_final_choices, init_bm25, generate_prompt_based_on_train_bm25
from preprocess.process_numeric_math import process_numeric_math
from preprocess.process_unit_math import preprocess_unit_math
from config import config
from transformers import BitsAndBytesConfig

PATH_TRAIN_CSV = "/hdd4/duongnh/project/ZaloAIChallenge/zalo_ai_2023_elementary_maths_solving/math_train.json"
PATH_TEST_CSV = "/hdd4/duongnh/project/ZaloAIChallenge/zalo_ai_2023_elementary_maths_solving/math_test_b.json"

file_test = open(PATH_TEST_CSV, 'r')
data_test = json.load(file_test)
file_train = open(PATH_TRAIN_CSV, 'r')
data_train = json.load(file_train)
bm25_index, l_data_with_explanation = init_bm25(data_train["data"])
l_submit_ids = []
l_submit_answers = []
# count = 0
# for idx, item in tqdm(enumerate(data_test["data"])):
#     id = item["id"]
#     status, answer_responce = preprocess_unit_math(item)
#     if status:
#         count += 1
#         print("Question: ", item["question"])
#         print("Choice: ", item["choices"])
#         print("Answer: ", answer_responce)
#         print("#####################")
#         l_submit_ids.append(id)
#         l_submit_answers.append(answer_responce)
# print(count)

count = 0
for idx, item in tqdm(enumerate(data_test["data"])):
    id = item["id"]
    status, answer_responce = process_numeric_math(item)
    if status:
        count += 1
        print("Question: ", item["question"])
        print("Choice: ", item["choices"])
        print("Answer: ", answer_responce)
        print("#####################")
        l_submit_ids.append(id)
        l_submit_answers.append(answer_responce)
print(count)