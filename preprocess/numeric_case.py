import re 
import unicodedata
import re
import unicodedata
import json 
import re, sys, json, os 
import re
import unicodedata
import re, sys, json, os 
import re
import unicodedata
import numpy as np

def convert_to_number(x):
    x=unicodedata.normalize("NFC", x).lower().replace("a.","").replace("b.","").replace("c.","").replace("d.","")
    x=x.replace("a:","").replace("b:","").replace("c:","").replace("d:","")
    x=x.replace(" ","").replace("x","*").replace(":","/").strip().replace("–","-")
    x=preprocess(x)
    x=case_hon_so(x)[0] # hon so
    x=case_phan_so(x)[0] # so thap phan
    return eval(x.strip().replace(",","."))


def case1(question_, choices_):
    
    re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', 'foobar')
    
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r"(.)*chữ số ([\d]+) trong số thập phân ([\d]+,*\s*([\d])+) là[:]*"
    regrex_pattern2 = r"(.)*chữ số ([\d]+) trong số ([\d]+,*\s*([\d])+) là[:]*"
    regrex_pattern3 = r"(.)*chữ số ([\d]+) trong số ([\d]+,*\s*([\d])+) có giá trị là[:]*"
    regrex_pattern4 = r"(.)*chữ số ([\d]+) trong số thập phân ([\d]+,*\s*([\d])+) có giá trị là[:]*"
    regrex_pattern5 = r"(.)*chữ số ([\d]+) trong.* ([\d]+,*\s*([\d])+).*là[:]*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)

#         if pattern_id==4:
#             print(question, choices)
        if len(matches) == 1:
            match = matches[0]
            # print(f"Found at case 1-pattern {pattern_id}")
            match = matches[0]
            phan_so = match.group(3).strip().replace(" ","")
            so = match.group(2)
            assert so in phan_so
#             if pattern_id==4:
#                 print(so, phan_so)
            phan_so = list(phan_so)
            index = phan_so.index(so)
            value_answer = ""
            for i in range(len(phan_so)):
                if i!= index and phan_so[i] not in ['.',',']:
                    value_answer +='0'
                elif phan_so[i] in ['.', ',']:
                    value_answer +='.'
                else:
                    value_answer += phan_so[i]
            value_answer = float(value_answer)
            try:
                choices = [convert_to_number(i) for i in choices]
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
#                 except Exception as e:
                return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern2,
        pattern_id=2
    )
    if out: return out
    out = match_pattern(
        regrex_pattern=regrex_pattern3,
        pattern_id=3
    )
    if out: return out
    out = match_pattern(
        regrex_pattern=regrex_pattern4,
        pattern_id=4
    )
    if out: return out
#     out = match_pattern(
#         regrex_pattern=regrex_pattern5,
#         pattern_id=5
#     )
#     if out: return out
    return []

def case2(question_, choices_):
    #     question  = unicodedata.normalize("NFC", question_).lower()
#     choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r"trong số ([\d]+,*([\d])+).*, chữ số ([\d]+) .* là[:]*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            match = matches[0]
            # print(f"Found at case 2-pattern {pattern_id}")
            match = matches[0]
            phan_so = match.group(1).strip().replace(" ","")
            so = match.group(3)
#             print(so, phan_so)
            assert so in phan_so

            phan_so = list(phan_so)
            index = phan_so.index(so)
            value_answer = ""
            for i in range(len(phan_so)):
                if i!= index and phan_so[i] not in ['.',',']:
                    value_answer +='0'
                elif phan_so[i] in ['.', ',']:
                    value_answer +='.'
                else:
                    value_answer += phan_so[i]
            value_answer = float(value_answer)
            try:
                choices = [convert_to_number(i) for i in choices]
        
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    return []


def case3(question_, choices_):
    
    
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
  
    regrex_pattern1 = r".*hỗn số (.*) được chuyển thành số thập phân.*"
    regrex_pattern2 = r".*hỗn số (.*) được viết dưới dạng số thập phân .*"
    regrex_pattern9= r".*hỗn số (.*) được đổi ra số thập phân.*"
    regrex_pattern10 = r".*hỗn số (.*) được viết thành số thập phân.*"
    
    
    regrex_pattern3 = r".*hỗn số (.*) được viết thành phân số.*"
    regrex_pattern4 = r".*hỗn số (.*) được đổi ra phân số.*"
    regrex_pattern11 = r".*hỗn số (.*) được viết dưới dạng phân số.*"
    regrex_pattern12 = r".*hỗn số (.*) được chuyển thành phân số.*"
    
    
    regrex_pattern5 = r".*hỗn số (.*) chuyển thành số thập phân.*"
    regrex_pattern6 = r".*hỗn số (.*) viết dưới dạng số thập phân .*"
    regrex_pattern7 = r".*hỗn số (.*) viết thành phân số.*"
    regrex_pattern8 = r".*hỗn số (.*) đổi ra phân số được.*"
    
    regrex_pattern13= r".*hỗn số (.*) đổi ra số thập phân.*"
    regrex_pattern14 = r".*hỗn số (.*) viết thành số thập phân.*"
    
    
    regrex_pattern15 = r".*hỗn số (.*) viết dưới dạng phân số.*"
    regrex_pattern16 = r".*hỗn số (.*) chuyển thành phân số.*"
    
    regrex_pattern17 = r".*hỗn số (.*) bằng số thập phân.*"
    regrex_pattern18 = r".*hỗn số (.*) bằng phân số.*"
    
    regrex_pattern17 = r".*hỗn số (.*) bằng số thập phân.*"
    regrex_pattern18 = r".*hỗn số (.*) bằng phân số.*"
    
    regrex_pattern19 = r".*hỗn số (.*) dưới dạng số thập phân.*"
    regrex_pattern20 = r".*hỗn số (.*) dưới dạng số phân số.*"
    regrex_pattern21 = r".*hỗn số (.*) thành số thập phân.*"
    regrex_pattern22 = r".*hỗn số (.*) thành phân số.*"
    
    # Chuyển hỗn số 4 \\frac{3}{5} thành phân số được:
#     Hỗn số 68  \\frac{7}{100}  dưới dạng số thập phân là:
    
#     Hỗn số 5 \\frac{1}{5} bằng số thập phân nào trong các số sau:
    
#     regrex_pattern5 = r".*\s*(.*) đổi ra phân số được.*"
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            match = matches[0]
            # print(f"Found at case 3-pattern {pattern_id}")
            match = matches[0]
            phan_so = match.group(1).strip().replace(" ","")
#             print(phan_so)
            phan_so  = convert_to_number(phan_so)
            value_answer = phan_so
#             print(value_answer)
            try:
                choices = [convert_to_number(i) for i in choices]
#                 print(choices)
#                 print([abs(value_answer-i) for i in choices] )
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
            
            
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern2,
        pattern_id=2
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern3,
        pattern_id=3
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern4,
        pattern_id=4
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern5,
        pattern_id=5
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern6,
        pattern_id=6
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern7,
        pattern_id=7
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern8,
        pattern_id=8
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern9,
        pattern_id=9
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern10,
        pattern_id=10
    )
    if out:return out
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern11,
        pattern_id=11
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern12,
        pattern_id=12
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern13,
        pattern_id=13
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern14,
        pattern_id=14
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern15,
        pattern_id=15
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern16,
        pattern_id=16
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern17,
        pattern_id=17
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern18,
        pattern_id=18
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern19,
        pattern_id=19
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern20,
        pattern_id=20
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern21,
        pattern_id=21
    )
    if out:return out
    out = match_pattern(
        regrex_pattern=regrex_pattern22,
        pattern_id=22
    )
    if out:return out
    return []

def case4(question_, choices_):
    #     question  = unicodedata.normalize("NFC", question_).lower()
#     choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    list_re = [
        r".*kết quả phép tính:* (.*) là:*",
        r".*kết quả phép cộng:* (.*) là:*",
        r".*kết quả phép trừ:* (.*) là:*",
        r".*kết quả phép nhân:* (.*) là:*",
        r".*kết quả phép chia:* (.*) là:*",
        
        r".*kết quả của phép tính:* (.*) là:*",
        r".*kết quả của phép cộng:* (.*) là:*",
        r".*kết quả của phép trừ:* (.*) là:*",
        r".*kết quả của phép nhân:* (.*) là:*",
        r".*kết quả của phép chia:* (.*) là:*",
        
        r".*kết quả phép tính:* (.*)",
        r".*kết quả phép cộng:* (.*)",
        r".*kết quả phép trừ:* (.*)",
        r".*kết quả phép nhân:* (.*)",
        r".*kết quả phép chia:* (.*)",
        
        r".*kết quả của phép tính:* (.*)",
        r".*kết quả của phép cộng:* (.*)",
        r".*kết quả của phép trừ:* (.*)",
        r".*kết quả của phép nhân:* (.*)",
        r".*kết quả của phép chia:* (.*)",
        
        
        r".*kết quả của phép tính:* (.*) = \?.*",
        r".*kết quả của phép cộng:* (.*) = \?.*",
        r".*kết quả của phép trừ:* (.*) = \?.*",
        r".*kết quả của phép nhân:* (.*) = \?.*",
        r".*kết quả của phép chia:* (.*) = \?.*",
        
        
        r".*kết quả của phép tính:* (.*) =.*",
        r".*kết quả của phép cộng:* (.*) =.*",
        r".*kết quả của phép trừ:* (.*) =.*",
        r".*kết quả của phép nhân:* (.*) =.*",
        r".*kết quả của phép chia:* (.*) =.*",
    ]
    
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            match = matches[0]
            # print(f"Found at case 4-pattern {pattern_id}")
            match = matches[0]
            value = match.group(1).strip().replace(" ","")
            value = preprocess(value)
            try:
                value_answer = convert_to_number(value)
            except Exception as e:
                return None
                
            try:
                choices = [convert_to_number(i) for i in choices]
#                 print(choices)
#                 print([abs(value_answer-i) for i in choices] )
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
        return None
    for index, r in enumerate(list_re):
        out = match_pattern(
            regrex_pattern=r,
            pattern_id=index+1
        )
        if out:
            return out
    return []

# được viết theo thứ tự từ bé đến lớn là
def case5(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r".*được viết theo thứ tự từ bé đến lớn là.*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            # print(f"Found at case 5-pattern {pattern_id}")
            choices = [i.replace("a.","").replace("b.","").replace("c.","").replace("d.","").strip() for i in choices]
#             print(choices)
            sep=';'  if ';' in choices[0] else ','
            choices = [i.split(sep) for i in choices]
#             print(choices)
            choices = [list(map(convert_to_number,i)) for i in choices]
            def check_is_sorted(x):
                x_ = sorted(x)
                if all([i<=j for i,j in zip(x, x[1:])]):
                    return True
                return False
            for i in range(len(choices)):
                if check_is_sorted(choices[i]):
                    return choices[i]
            return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    return []

def case6(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r".*được viết theo thứ tự từ lớn đến bé là.*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            # print(f"Found at case 6-pattern {pattern_id}")
            choices = [i.replace("a.","").replace("b.","").replace("c.","").replace("d.","").strip() for i in choices]
#             print(choices)
            sep=';'  if ';' in choices[0] else ','
            choices = [i.split(sep) for i in choices]
#             print(choices)
            choices = [list(map(convert_to_number,i)) for i in choices]
            def check_is_sorted(x):
                x_ = sorted(x)
                if all([i>=j for i,j in zip(x, x[1:])]):
                    return True
                return False
            for i in range(len(choices)):
                if check_is_sorted(choices[i]):
                    return choices[i]
            return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    return []

# được viết theo thứ tự từ bé đến lớn là
def case7(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r".*kết quả của biểu thức:* (.*) là:*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            # print(f"Found at case 7-pattern {pattern_id}")
            match = matches[0]
            value = match.group(1).strip().replace(" ","")
            value = preprocess(value)
            try:
                value_answer = convert_to_number(value)
            except Exception as e:
                return None
            try:
                choices = [convert_to_number(i) for i in choices]
#                 print(choices)
#                 print([abs(value_answer-i) for i in choices] )
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
            
            return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    return []

# được viết theo thứ tự từ bé đến lớn là
def case8(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    list_re = [
        r".*số lớn nhất trong các số: (.*) là:*",
        r".*số lớn nhất trong các số: (.*)",
        r".*số lớn nhất trong các số (.*) là:*",
        r".*số lớn nhất trong các số (.*)",
        
        
        r".*số nào lớn nhất trong các số: (.*) là:*",
        r".*số nào lớn nhất trong các số: (.*)",
        r".*số nào lớn nhất trong các số (.*) là:*",
        r".*số nào lớn nhất trong các số (.*)",
        
    ]
#     regrex_pattern1 = r".*được viết theo thứ tự từ bé đến lớn là.*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            value = matches[0].group(1)
            sep=';' if ';' in value else ','
            value = value.strip().split(sep)
            try:
                value = list(map(convert_to_number, value))
            except Exception as e:
                pass
                #print(question, choices, e, 'case 8')
#             value = list(map(convert_to_number, value))
            index_max = np.argmax(value)
            value_answer = value[index_max]
            try:
                choices = [convert_to_number(i) for i in choices]
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
            
            return None
        return None
    for index, r in enumerate(list_re):
        out = match_pattern(
            regrex_pattern=r,
            pattern_id=index+1
        )
        if out:
            return out
    return []

def case6(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    
    regrex_pattern1 = r".*được viết theo thứ tự từ lớn đến bé là.*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            # print(f"Found at case 6-pattern {pattern_id}")
            choices = [i.replace("a.","").replace("b.","").replace("c.","").replace("d.","").strip() for i in choices]
#             print(choices)
            sep=';'  if ';' in choices[0] else ','
            choices = [i.split(sep) for i in choices]
#             print(choices)
            choices = [list(map(convert_to_number,i)) for i in choices]
            def check_is_sorted(x):
                x_ = sorted(x)
                if all([i>=j for i,j in zip(x, x[1:])]):
                    return True
                return False
            for i in range(len(choices)):
                if check_is_sorted(choices[i]):
                    return choices[i]
            return None
        return None
    out = match_pattern(
        regrex_pattern=regrex_pattern1,
        pattern_id=1
    )
    if out:return out
    return []

def case9(question_, choices_):
    question  = unicodedata.normalize("NFC", question_).lower()
    question = re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', question)
    
    choices = [unicodedata.normalize("NFC", i).lower() for i in choices_]
    choices = [re.sub(r'(\d+)\s+(\d+)', r'\g<1>\g<2>', i) for i in choices]
    # Check pattern 1: Giá trị của chữ số 9 trong số thập phân 0,09 là:
    # Giá trị của chữ số 9 trong số thập phân 0,09 là:
    list_re = [
        r".*số bé nhất trong các số: (.*) là:*",
        r".*số bé nhất trong các số: (.*)",
        r".*số bé nhất trong các số (.*) là:*",
        r".*số bé nhất trong các số (.*)",
        
        
        r".*số nào bé nhất trong các số: (.*) là:*",
        r".*số nào bé nhất trong các số: (.*)",
        r".*số nào bé nhất trong các số (.*) là:*",
        r".*số nào bé nhất trong các số (.*)",
        
    ]
#     regrex_pattern1 = r".*được viết theo thứ tự từ bé đến lớn là.*"
#     chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là
    def match_pattern(regrex_pattern, pattern_id=1, question=question, choices=choices, choices_=choices_):
        regrex_pattern = unicodedata.normalize("NFC", regrex_pattern)
        matches = re.finditer(regrex_pattern, question, re.MULTILINE)
        matches = list(matches)


        if len(matches) == 1:
            # print(f"Found at case 9-pattern {pattern_id}")
            
            value = matches[0].group(1)
            sep=';' if ';' in value else ','
            value = value.strip().split(sep)
            try:
                value = list(map(convert_to_number, value))
            except Exception as e:
                # print(question, choices, e, 'case 9')
                pass
            index_max = np.argmin(value)
            value_answer = value[index_max]
            try:
                choices = [convert_to_number(i) for i in choices]
#                 print(choices)
#                 print([abs(value_answer-i) for i in choices] )
                index_answer = -1
                for index, i in enumerate(choices):
                    if abs(value_answer - i) <= 1e-6:
                        index_answer = index
                return choices_[index_answer]
            except Exception as e:
                return None
            
            return None
        return None
    for index, r in enumerate(list_re):
        out = match_pattern(
            regrex_pattern=r,
            pattern_id=index+1
        )
        if out:
            return out
    return []


def preprocess(text):
    text = unicodedata.normalize("NFC", text)
    time_convert  = '${\\times}$'
    text =text.replace(time_convert, "*")
    text = text.replace("\\left", "").replace("\\right","").replace("\\div","/").replace("\\\times","*").replace("\\times","*")
    text = text.replace("\\\\left", "").replace("\\\\right","").replace("\\\\div","/").replace("\\\times","*").replace("\\times","*")
    div = r'([\d]+) : ([\d]+)'
    text = re.sub(div, r'\g<1>/\g<2>',text).replace("$","")
    return text
# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

def case_hon_so(test_str):
    """hỗn số $57\\frac{1}{6}$ ->343/6"""
    regex = r"[\$]*[\\]*([\d]+)[\\]*\\frac\{([0-9]+)\}\{([0-9]+)}[\$]*"
    test_str=unicodedata.normalize("NFC", test_str)
    matches = re.finditer(regex, test_str, re.MULTILINE)
    contexts = []
    new_text = ""
    previous = 0
    for matchNum, match in enumerate(matches, start=1):
        num = 0
        assert len(match.groups()) == 3
        num = float(match.group(1)) + float(match.group(2)) / float(match.group(3))
        ps = float(match.group(1)) * float(match.group(3)) + float(match.group(2))
        if int(ps) == ps:
            ps = int(ps)
        
        value = float(ps) / float(match.group(3))
        num = str(f'{ps}/{match.group(3)}')
        contexts.append(
            f"biết {num} có giá trị là {value}"
        )
        new_text = new_text + test_str[previous:int(match.start())] 
        new_text = new_text + num 
        previous = int(match.end())
    new_text = new_text + test_str[previous:]
    return new_text, list(set(contexts))
def case_phan_so(test_str):
    """chuyển phần số dạng frac sang / 
    """
    regex = r"[\$]*[\\]*\\frac\{([0-9]+)\}\{([0-9]+)}[\$]*"
    test_str=unicodedata.normalize("NFC", test_str)
    matches = re.finditer(regex, test_str, re.MULTILINE)
    contexts = []
    new_text = ""
    previous = 0
    for matchNum, match in enumerate(matches, start=1):
        num = 0
        assert len(match.groups()) == 2
        num = float(match.group(1)) / float(match.group(2))
        ps = float(match.group(1))
        if int(ps) == ps:
            ps = int(ps)
        
        value = float(ps) / float(match.group(2))
        num = str(f'{ps}/{match.group(2)}')
        contexts.append(
            f"biết {num} có giá trị là {value}"
        )
        new_text = new_text + test_str[previous:int(match.start())] 
        new_text = new_text + num 
        previous = int(match.end())
    new_text = new_text + test_str[previous:]
    return new_text, list(set(contexts))




def case_one(test_str):
    
    test_str = unicodedata.normalize("NFC", test_str).lower().replace("là:","là").strip()
    # print(test_str, " case one")
    regex = r"chữ số ([\d]+) trong số ([\d]+,[\d]+) có giá trị là"

    # test_str = "chữ số 7 trong số 291,725 có giá trị là"

    matches = re.finditer(regex, test_str, re.MULTILINE)
    matches = list(matches)
    assert len(matches) == 1, matches
    match = matches[0]
    var = float(match.group(1))
    assert var == int(var), var
    var = match.group(1)
    start = 0
    target = match.group(2)
    target = list(target)
    while start < len(target) and target[start] != var:
        if target[start]!=',':
            target[start] = '0'
        start += 1
    start_ = start+1
    while start_ < len(target):
        target[start_]='0'
        start_+=1
    target = "".join(target).replace(",",".")
    target = float(target)
    return target

def case_two(test_str):
    
    # test_str = unicodedata.normalize("NFC", test_str).lower().replace("là:","là").strip()
    # print(test_str, " case one")
    regex = regex = r"((hỗn số)|(phân số)) (.*) ((được chuyển thành số thập phân là)|(được viết dưới dạng số thập phân là)|(được viết thành phân số là)|(đổi ra phân số được)|(được viết dưới dạng số thập phân là))"
    regex = unicodedata.normalize("NFC", regex)
    test_str=unicodedata.normalize("NFC", test_str).lower().replace(":","")

    # test_str = "chữ số 7 trong số 291,725 có giá trị là"

    matches = re.finditer(regex, test_str, re.MULTILINE)
    matches = list(matches)
    assert len(matches) == 1, matches
    match = matches[0]
    var = match.group(4)
    var = preprocess(var)
    var, _ =case1(var)
    var, _ = case2(var)
    var = var.replace(",",".")
    return eval(var)

def case_three(test_str):
    regex = r"phần nguyên của (số|thập phân) (.*) là"
    regex = unicodedata.normalize("NFC", regex)
    test_str=unicodedata.normalize("NFC", test_str).lower().replace(":","")
    matches = re.finditer(regex, test_str, re.MULTILINE)
    matches = list(matches)
    assert len(matches) == 1, matches
    match = matches[0]
    var = match.group(2)
    var = preprocess(var)
    var, _ =case1(var)
    var, _ = case2(var)
    var = var.replace(",",".").replace("thập phân","").strip()
    return int(eval(var))

def to_num(x):
    x=x.replace("A.","").replace("B.","").replace("C.", "").replace("D.","").replace("E.","")
    
    x=[ix for ix in x if ix in '0123456789,./+-*']
    x ="".join(x).strip().replace(",",".")
    return eval(x)

def try_case(i, case_function, is_try=True):
    if is_try:
        try:
            
            target = case_function(i['question'])
            choices = [preprocess(ix) for ix in i['choices']]
            correct=None 
            for ix in range(len(choices)):
                choices[ix], _ = case1(choices[ix])
                choices[ix], _ = case2(choices[ix])
                if abs(to_num(choices[ix]) - target) < 1e-4:
                    correct = ix
            return i['choices'][correct]
        except Exception as e:
            return None 
    else:
        target = case_function(i['question'])
        # print(target, " target")
        choices = [preprocess(ix) for ix in i['choices']]
        correct=None 
        for ix in range(len(choices)):
            choices[ix], _ = case1(choices[ix])
            choices[ix], _ = case2(choices[ix])
            # print(to_num(choices[ix]))
            if abs(to_num(choices[ix]) - target) < 1e-4:
                correct = ix
        return i['choices'][correct]
    


