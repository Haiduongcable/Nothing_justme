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
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import os
import pandas as pd
from utils import generate_prompt_based_on_train, get_final_choices
from preprocess.process_numeric_math import process_numeric_math
from preprocess.process_unit_math import preprocess_unit_math
from config import config
from transformers import BitsAndBytesConfig
model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
if config["DELOY_KAGGLE"]:
    PATH_TRAIN_CSV = "/kaggle/input/zalo-ai-2023-elementaty-maths-solving/zalo_ai_2023_elementary_maths_solving/math_train.json"
    PATH_TEST_CSV = "/kaggle/input/zalo-ai-2023-elementaty-maths-solving/zalo_ai_2023_elementary_maths_solving/math_test.json"
else:
    PATH_TRAIN_CSV = "data/math_train.json"
    PATH_TEST_CSV = "data/math_test.json"
search_faiss = read_index("train.index")
model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base', device = torch.device("cpu"))

if config["USE_MODEL"]:
    

    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-14B", trust_remote_code=True)
    max_memory_mapping = {0: "16GB"}
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-14B",
                                                quantization_config,
                                                device_map="auto",
                                                trust_remote_code=True,
                                                max_memory=max_memory_mapping).eval()

prefix_prompt = '''
You are a virtual assistant capable of answering math questions honestly and accurately, without fabricating additional content.
Based on the following multiple choice questions, let's think step by step, come up with a solution and choose the correct answer.

Question:
Một người bán hàng bỏ ra 80,000 đồng tiền vốn và bị lỗ 6%. Để tính số tiền lỗ ta phải tính?
Options:
A. 80,000 : 6
B. 80,000 x 6
C. 80,000 : (6 x 100)
D. (80,000 x 6) : 100
Solution: Theo đề bài, số tiền lỗ bằng 6% của 80 000 đồng . Để tìm số tiền lỗ ta có thể lấy 80 000 chia cho 100 rồi nhân với 6 (tức là 80 000 : 100 × 6) hoặc lấy 80000 nhân với 6 rồi chia cho 100 (tức là 80 000 × 6 : 100).
Correct answer: D. (80,000 x 6) : 100

Question:
8 dm2 24 cm2 = ……… dm2. Số thích hợp điền vào chỗ chấm là?
Options:
A. 824
B. 82,4
C. 8,24
D. 0,824
Solution: Ta có 24 cm2 = 0,24 dm2 Vậy 8 dm2 24 cm2 = 8,24 dm2.
Correct answer: C. 8,24

Question:
10% của 11,5m2 là?
Options:
A. 10,15dm2
B. 1,5m2
C. 15,5m2
D. 1,15m2
Solution: 10% của 11,5m2 là: 11,5 ${\\times}$ 10 : 100 = 1,15 (m2).
Correct answer: D. 1,15m2
'''

file_test = open(PATH_TEST_CSV, 'r')
data_test = json.load(file_test)
file_train = open(PATH_TRAIN_CSV, 'r')
data_train = json.load(file_train)
l_submit_ids = []
l_submit_answers = []
for idx, item in tqdm(enumerate(data_test["data"])):
    id = item["id"]
    try:
        status, answer_responce = preprocess_unit_math(item)
        if status:
            l_submit_ids.append(id)
            l_submit_answers.append(answer_responce)
            continue
        
    except:
        pass
    try:
        status, answer_responce = process_numeric_math(item)
        if status:
            l_submit_ids.append(id)
            l_submit_answers.append(answer_responce)
            continue
    except:
        pass
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
    
    prompt = generate_prompt_based_on_train(question,\
                                            choices_str,\
                                            search_faiss,\
                                            model_embedding,\
                                            prefix_prompt,\
                                            data_train["data"])
    if config["USE_MODEL"]:
        inputs = tokenizer([prompt], return_tensors="pt").to('cuda')
        res = model.generate(**inputs,  max_new_tokens=200,temperature=0.01)
        output = tokenizer.decode(res.cpu()[0], skip_special_tokens=True)
        answer_responce = get_final_choices(item, output)
        l_submit_ids.append(id)
        l_submit_answers.append(answer_responce)
    else:
        l_submit_ids.append(id)
        l_submit_answers.append(item["choices"][0])

df_submit = pd.DataFrame()

df_submit["id"] = l_submit_ids
df_submit["answer"] = l_submit_answers
df_submit.to_csv("result/submission.csv", index = False)