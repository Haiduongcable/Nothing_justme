import os 
import numpy as np 
from tqdm import tqdm 
import json 
import cv2 
import math 
import pandas as pd 
from preprocess.unit_case import handle_distance, handle_area, handle_volume, handle_weight, handle_time
import difflib
from preprocess.vietnamese_preprocess import tien_xu_li
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
