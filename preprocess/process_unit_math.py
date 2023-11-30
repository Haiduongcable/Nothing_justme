import os 
import numpy as np 
from tqdm import tqdm 
import json 
import cv2 
import math 
import pandas as pd 
from process_unit_math import handle_distance, handle_area, handle_volume, handle_weight, handle_time
import difflib
from vietnamese_preprocess import tien_xu_li
import sys


def process_unit_case(question_str):
    found_d, result = handle_distance(question_str)
    if found_d:
        return True, result
    found_a, result = handle_area(question_str)
    if found_a:
        return True, result
        
    found_v, result = handle_volume(question_str)
    if found_v:
        return True, result
    found_w, result = handle_weight(question_str)
    if found_w:
        return True, result
    found_t, result = handle_time(question_str)
    if found_t:
        return True, result
    return False, None

def check_string_is_digit(input_str):
    #check is float or int 
    try:
        float_val = float(input_str)
        return True
    except ValueError:
        if input_str.isdigit():
            return True
        elif input_str.isnumeric():
            return True
        else:
            return False
        
def compare_value(result, cleaned_choices):
    selected_idx = -1 
    min_value = sys.maxsize
    for idx, choice in enumerate(cleaned_choices):
        diff_value = abs(result - choice)
        if diff_value < min_value:
            min_value  = diff_value
            selected_idx = idx   
    return selected_idx 

def compare_string(result, cleaned_choices):
    close_matches = difflib.get_close_matches(str(result), 
                cleaned_choices, 1, 0)[0]
    return  cleaned_choices.index(close_matches)

# def selected_answer_and_compare(l_choices, result):
#     cleaned_str_choices = []
#     cleaned_numeric_choices = []
#     # NẾU XỬ LÝ ĐƯỢC -> SO SÁNH NGANG HÀNG, NẾU KO -> SO SÁNH 
#     l_remove = ["a.", "b.", "c.", "d."]
#     for choice in l_choices:
#         choice = choice.lower()
#         for word_remove in l_remove:
#             choice = choice.replace(word_remove, "")
#         choice = choice.replace(" ", "").replace(",", ".")
#         if check_string_is_digit(choice):
#             cleaned_numeric_choices.append(float(choice))
#         cleaned_str_choices.append(choice)
#     if len(cleaned_numeric_choices) == len(choice):
#         #compare the same
#         selected_idx = compare_value(result, cleaned_numeric_choices)
#     else:
#         selected_idx = compare_string(result, cleaned_str_choices)
#     return selected_idx

def preprocess_unit_math(item):
    '''
    Return status and answer
    '''
    question = item["question"]
    question_str = question.replace("\n", "").replace("\t", "").lower()
    question_str = tien_xu_li(question_str)
    choices = item["choices"]
    status, result = process_unit_case(question_str)
    cleaned_str_choices = []
    cleaned_numeric_choices = []
    l_remove = ["a.", "b.", "c.", "d."]
    for choice in choices:
        choice = choice.lower()
        for word_remove in l_remove:
            choice = choice.replace(word_remove, "")
        choice = choice.replace(" ", "").replace(",", ".")
        if check_string_is_digit(choice):
            cleaned_numeric_choices.append(float(choice))
        cleaned_str_choices.append(choice)
    if not status:
        return False, None 
    if status: 
        if check_string_is_digit(result) and len(cleaned_numeric_choices) == len(choices):
            #return float -> find 
            selected_idx = compare_value(result, cleaned_numeric_choices)
        else:
            selected_idx = compare_string(result, cleaned_str_choices)
        return True, choices[selected_idx]
    
# question_str = "Số thích hợp cần điền vào chỗ chấm để 45,5 giờ = …….giờ ....phút là "
# status, result = process_unit_case(question_str)
# print(result)
# print(round(result, 6))
# l_used_id = []
# # path_submit = "/hdd4/duongnh/project/ZaloAIChallenge/output_submit"
# # # for nfile in os.listdir(path_submit):
file_test = open("/hdd4/duongnh/project/ZaloAIChallenge/zalo_ai_2023_elementary_maths_solving/math_train.json", 'r')
data_test = json.load(file_test)["data"]
count = 0
for idx, item in enumerate(data_test):
    status, answer_responce = preprocess_unit_math(item)
#     # # if idx != 319:
#     # #     continue
#     # question = item["question"]
#     # question_str = question.replace("\n", "").replace("\t", "").lower()
#     # question_str = tien_xu_li(question_str)
#     # choices = item["choices"]
#     # status, result = process_unit_case(question_str)
    if status:
        label_choice = item["answer"]
        if label_choice != answer_responce:
            print("IDX: ", idx)
            print("Question: ", item["question"])
            print(item["choices"])
            print("__________")
            print("Result: ", answer_responce)
            print("Labels: ", label_choice)
        count += 1
print("Count: ", count)


# with open("/hdd4/duongnh/project/ZaloAIChallenge/temp/ignore_id.txt", 'a') as file:
#     for idx in l_used_id:
#         file.write(str(idx) + "\n")
# file.close()

# df_out = pd.DataFrame()
# df_out["id"] = l_ids
# df_out["answer"] = l_answer
# df_out.to_csv("/hdd4/duongnh/project/ZaloAIChallenge/output_submit/submission_qwen_14b_best_28_11_update_v2.csv", index = False)
# # print("Done")

'''
xử lý dạng 300 000 đã 

Khử các case sau: cộng trừ nhân chia/ có số 
Hoặc là dạng 3km 5dm 6hm (éo hiểu thằng cặc nào nghĩ ra case này)


Xử luôn case mà cộng trừ nhân chia 

Xử luôn case mà dùng đến phép chia

Xử case dùng đến thời gian, tốc độ, gia tốc (chơi hết).
Destroy chúng nó. 

Xử luôn case giá trị/ kết quả của biểu thức: (câu này xuất hiện 30 lần trong train với nhiều hình dạng khác nhau)

'''