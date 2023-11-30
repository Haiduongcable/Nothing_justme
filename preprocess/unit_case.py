import re


def build_convert_unit_table(l_units, range_value = 10):
    dict_convert = {}
    num_unit = len(l_units)
    for idx_s in range(num_unit):
        for idx_d in range(num_unit):
            value = pow(range_value, idx_s - idx_d)
            dict_convert[l_units[idx_s], l_units[idx_d]] = value
    return dict_convert

def check_valid_matched(current_matched_str, question_str):
    '''
    previous is a digit: 
    previous char is: +, -
    
    '''
    tmp_plus_minus = ["+", "-", "–"]
    end_idx = question_str.index(current_matched_str)
    if end_idx == 0:
        return True 
    elif end_idx == 1:
        checking_char = question_str[0]
        if checking_char.isdecimal():
            return False
        if checking_char in tmp_plus_minus:
            return False
    else:
        #tmp_check = 
        checking_str = question_str[end_idx-2:end_idx]
        checking_str = checking_str.replace(" ", "")
        if checking_str.isdecimal():
            return False
        if checking_str in tmp_plus_minus:
            return False
    
    return True

def rulebase_fill_in_distance_case_1(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["mm", "cm", "dm", "m", "dam", "hm", "km"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"\b(\d+\s*(mm|cm|dm|m|dam|hm|km)\s*\d*\s*(mm|cm|dm|m|dam|hm|km)\s*=\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km))\b"
    pattern_find_value = r"(\d+)\s*(mm|cm|dm|m|dam|hm|km)"
    matches = re.findall(pattern_search, question_str)
    result = ""
    found = False
    if matches:
        matches = matches[0]
        math_sentece = matches[0]
        des_unit = matches[-1]
        matches_value = re.findall(pattern_find_value, math_sentece)
        if matches_value and len(matches_value) == 2:
            value__src_0, unit_src_0 = matches_value[0]
            value_src_1, unit__src_1 = matches_value[1]
            result = int(value__src_0) * dict_convert[unit_src_0, des_unit] +\
                     int(value_src_1) * dict_convert[unit__src_1, des_unit]
            if  isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(math_sentece, question_str):
                found = True 
            else:
                found = False
            
    return found, result


def rulebase_fill_in_distance_case_2(question_str):
    l_units = ["mm", "cm", "dm", "m", "dam", "hm", "km"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    l_pattern = [r"(\d{1,3}(?:\s\d{3})*)(?:\s*)?(mm|cm|dm|m|dam|hm|km)\s*=\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km)", 
                 r"(\d{1,3}(?:\s\d{3})*(?:\s\d{3})*)\s*(mm|cm|dm|m|dam|hm|km)\s*=\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km)"]
    found = False 
    result = ""
    for pattern_search in l_pattern:
        match = re.search(pattern_search, question_str)
        if match:
            value = match.group(1).replace(" ", "") 
            unit_src = match.group(2)
            unit_des = match.group(3)
            result = float(value) * dict_convert[unit_src, unit_des] 
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            if check_valid_matched(match.group(1), question_str):
                found = True 
                break
            else:
                found = False
            
            
    return found, result


def rulebase_fill_in_distance_case_3(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["mm", "cm", "dm", "m", "dam", "hm", "km"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm|cm|dm|m|dam|hm|km)\s*=\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km)"
    match = re.search(pattern_search, question_str)
    found = False 
    result = ""
    if match:
        value = match.group(1)
        unit_src = match.group(2)
        unit_des = match.group(3)
        value = str(value).replace(",", ".")
        result = float(value) * dict_convert[unit_src, unit_des] 
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False
            
    return found, result

def rulebase_fill_in_distance_case_4(question_str):
    l_units = ["mm", "cm", "dm", "m", "dam", "hm", "km"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm|cm|dm|m|dam|hm|km)\s*=\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km)\s*[\.,… _*#]*\s*(mm|cm|dm|m|dam|hm|km)\b"
    match = re.search(pattern_search, question_str)
    found = False
    result_str = ""
    if match:
        value1 = match.group(1).replace(",", ".")  # Replace comma with dot for decimal values
        unit_src = match.group(2)
        unit_des_1 = match.group(3)
        unit_des_2 = match.group(4)
        num_des_1 = int(float(value1) * dict_convert[unit_src, unit_des_1])
        num_des_2 = int(round((float(value1) * dict_convert[unit_src, unit_des_1] - num_des_1) * dict_convert[unit_src, unit_des_2]))
        result_str = str(num_des_1) + " " + unit_des_1 + " " + str(num_des_2) + " " + unit_des_2
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False 
    return found, result_str


            

def rulebase_fill_in_area_case_1(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    ha -> hm2
    '''
    
    l_units = ["mm2", "cm2", "dm2", "m2", "dam2", "hm2", "km2"]
    dict_convert = build_convert_unit_table(l_units, range_value = 100)
    pattern_search = r"\b(\d+\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*\d*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*=\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2))\b"
    pattern_find_value = r"(\d+)\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)"
    matches = re.findall(pattern_search, question_str)
    result = ""
    found = False
    if matches:
        matches = matches[0]
        math_sentece = matches[0]
        des_unit = matches[-1]
        matches_value = re.findall(pattern_find_value, math_sentece)
        if matches_value and len(matches_value) == 2:
            value__src_0, unit_src_0 = matches_value[0]
            value_src_1, unit__src_1 = matches_value[1]
            result = int(value__src_0) * dict_convert[unit_src_0, des_unit] +\
                     int(value_src_1) * dict_convert[unit__src_1, des_unit]
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(math_sentece, question_str):
                found = True
            else:
                found = False
            
    return found, result

def rulebase_fill_in_area_case_2(question_str):
    l_units = ["mm2", "cm2", "dm2", "m2", "dam2", "hm2", "km2"]
    dict_convert = build_convert_unit_table(l_units, range_value = 100)
    l_pattern = [r"(\d{1,3}(?:\s\d{3})*)(?:\s*)?(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*=\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)", 
                 r"(\d{1,3}(?:\s\d{3})*(?:\s\d{3})*)\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*=\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)"]
    found = False 
    result = ""
    for pattern_search in l_pattern:
        match = re.search(pattern_search, question_str)
        if match:
            value = match.group(1).replace(" ", "") 
            unit_src = match.group(2)
            unit_des = match.group(3)
            result = float(value) * dict_convert[unit_src, unit_des] 
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(match.group(1), question_str):
                found = True
                break
            else:
                found = False
            
            
    return found, result

def rulebase_fill_in_area_case_3(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["mm2", "cm2", "dm2", "m2", "dam2", "hm2", "km2"]
    dict_convert = build_convert_unit_table(l_units, range_value = 100)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*=\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)"
    match = re.search(pattern_search, question_str)
    found = False 
    result = ""
    if match:
        value = match.group(1)
        unit_src = match.group(2)
        unit_des = match.group(3)
        value = str(value).replace(",", ".")
        result = float(value) * dict_convert[unit_src, unit_des]
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        if check_valid_matched(match.group(1), question_str):
            found = True
        else:
            found = False
            
    return found, result

def rulebase_fill_in_area_case_4(question_str):
    l_units = ["mm2", "cm2", "dm2", "m2", "dam2", "hm2", "km2"]
    dict_convert = build_convert_unit_table(l_units, range_value = 100)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*=\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\s*[\.,… _*#]*\s*(mm2|cm2|dm2|m2|dam2|hm2|km2)\b"
    match = re.search(pattern_search, question_str)
    found = False
    result_str = ""
    if match:
        value1 = match.group(1).replace(",", ".")  # Replace comma with dot for decimal values
        unit_src = match.group(2)
        unit_des_1 = match.group(3)
        unit_des_2 = match.group(4)
        num_des_1 = int(float(value1) * dict_convert[unit_src, unit_des_1])
        num_des_2 = int(round((float(value1) * dict_convert[unit_src, unit_des_1] - num_des_1) * dict_convert[unit_src, unit_des_2]))
        result_str = str(num_des_1) + " " + unit_des_1 + " " + str(num_des_2) + " " + unit_des_2
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False 
    return found, result_str

def rulebase_fill_in_volume_case_1(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    ha -> hm2
    '''
    
    l_units = ["mm3", "cm3", "dm3", "m3", "dam3", "hm3", "km3"]
    dict_convert = build_convert_unit_table(l_units, range_value = 1000)
    pattern_search = r"\b(\d+\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*\d*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*=\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3))\b"
    pattern_find_value = r"(\d+)\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)"
    matches = re.findall(pattern_search, question_str)
    result = ""
    found = False
    if matches:
        matches = matches[0]
        math_sentece = matches[0]
        des_unit = matches[-1]
        matches_value = re.findall(pattern_find_value, math_sentece)
        if matches_value and len(matches_value) == 2:
            value__src_0, unit_src_0 = matches_value[0]
            value_src_1, unit__src_1 = matches_value[1]
            result = int(value__src_0) * dict_convert[unit_src_0, des_unit] +\
                     int(value_src_1) * dict_convert[unit__src_1, des_unit]
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(math_sentece, question_str):
                found = True
            else:
                found = False
            
    return found, result

def rulebase_fill_in_volume_case_2(question_str):
    l_units = ["mm3", "cm3", "dm3", "m3", "dam3", "hm3", "km3"]
    dict_convert = build_convert_unit_table(l_units, range_value = 1000)
    l_pattern = [r"(\d{1,3}(?:\s\d{3})*)(?:\s*)?(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*=\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)", 
                 r"(\d{1,3}(?:\s\d{3})*(?:\s\d{3})*)\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*=\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)"]
    found = False 
    result = ""
    for pattern_search in l_pattern:
        match = re.search(pattern_search, question_str)
        if match:
            value = match.group(1).replace(" ", "") 
            unit_src = match.group(2)
            unit_des = match.group(3)
            result = float(value) * dict_convert[unit_src, unit_des] 
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(match.group(1), question_str):
                found = True
                break
            else:
                found = False
            
    return found, result

def rulebase_fill_in_volume_case_3(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["mm3", "cm3", "dm3", "m3", "dam3", "hm3", "km3"]
    dict_convert = build_convert_unit_table(l_units, range_value = 1000)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*=\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)"
    match = re.search(pattern_search, question_str)
    found = False 
    result = ""
    if match:
        value = match.group(1)
        unit_src = match.group(2)
        unit_des = match.group(3)
        value = str(value).replace(",", ".")
        result = float(value) * dict_convert[unit_src, unit_des] 
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        if check_valid_matched(match.group(1), question_str):
            found = True
        else:
            found = False 
    
    return found, result

def rulebase_fill_in_volume_case_4(question_str):
    l_units = ["mm3", "cm3", "dm3", "m3", "dam3", "hm3", "km3"]
    dict_convert = build_convert_unit_table(l_units, range_value = 1000)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*=\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\s*[\.,… _*#]*\s*(mm3|cm3|dm3|m3|dam3|hm3|km3)\b"
    match = re.search(pattern_search, question_str)
    found = False
    result_str = ""
    if match:
        value1 = match.group(1).replace(",", ".")  # Replace comma with dot for decimal values
        unit_src = match.group(2)
        unit_des_1 = match.group(3)
        unit_des_2 = match.group(4)
        num_des_1 = int(float(value1) * dict_convert[unit_src, unit_des_1])
        num_des_2 = int(round((float(value1) * dict_convert[unit_src, unit_des_1] - num_des_1) * dict_convert[unit_src, unit_des_2]))
        result_str = str(num_des_1) + " " + unit_des_1 + " " + str(num_des_2) + " " + unit_des_2
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False 
    return found, result_str

def rulebase_fill_in_weight_case_1(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    ha -> hm2
    '''
    
    l_units = ["g", "dag", "hg", "kg", "yến", "tạ", "tấn"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"\b(\d+\s*(g|dag|hg|kg|yến|tạ|tấn)\s*\d*\s*(g|dag|hg|kg|yến|tạ|tấn)\s*=\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn))\b"
    pattern_find_value = r"(\d+)\s*(g|dag|hg|kg|yến|tạ|tấn)"
    matches = re.findall(pattern_search, question_str)
    result = ""
    found = False
    if matches:
        matches = matches[0]
        math_sentece = matches[0]
        des_unit = matches[-1]
        matches_value = re.findall(pattern_find_value, math_sentece)
        if matches_value and len(matches_value) == 2:
            value__src_0, unit_src_0 = matches_value[0]
            value_src_1, unit__src_1 = matches_value[1]
            result = int(value__src_0) * dict_convert[unit_src_0, des_unit] +\
                     int(value_src_1) * dict_convert[unit__src_1, des_unit]
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(math_sentece, question_str):
                found = True
            else:
                found = False 
            
    return found, result

def rulebase_fill_in_weight_case_2(question_str):
    l_units = ["g", "dag", "hg", "kg", "yến", "tạ", "tấn"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    l_pattern = [r"(\d{1,3}(?:\s\d{3})*)(?:\s*)?(g|dag|hg|kg|yến|tạ|tấn)\s*=\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn)", 
                 r"(\d{1,3}(?:\s\d{3})*(?:\s\d{3})*)\s*(g|dag|hg|kg|yến|tạ|tấn)\s*=\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn)"]
    found = False 
    result = ""
    for pattern_search in l_pattern:
        match = re.search(pattern_search, question_str)
        if match:
            value = match.group(1).replace(" ", "") 
            unit_src = match.group(2)
            unit_des = match.group(3)
            result = float(value) * dict_convert[unit_src, unit_des] 
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(match.group(1), question_str):
                found = True
                break
            else:
                found = False 
         
    return found, result

def rulebase_fill_in_weight_case_3(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["g", "dag", "hg", "kg", "yến", "tạ", "tấn"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(g|dag|hg|kg|yến|tạ|tấn)\s*=\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn)"
    match = re.search(pattern_search, question_str)
    found = False 
    result = ""
    if match:
        value = match.group(1)
        unit_src = match.group(2)
        unit_des = match.group(3)
        value = str(value).replace(",", ".")
        result = float(value) * dict_convert[unit_src, unit_des] 
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        if check_valid_matched(match.group(1), question_str):
            found = True
        else:
            found = False 
            
    return found, result

def rulebase_fill_in_weight_case_4(question_str):
    l_units = ["g", "dag", "hg", "kg", "yến", "tạ", "tấn"]
    dict_convert = build_convert_unit_table(l_units, range_value = 10)
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(g|dag|hg|kg|yến|tạ|tấn)\s*=\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn)\s*[\.,… _*#]*\s*(g|dag|hg|kg|yến|tạ|tấn)\b"
    match = re.search(pattern_search, question_str)
    found = False
    result_str = ""
    if match:
        value1 = match.group(1).replace(",", ".")  # Replace comma with dot for decimal values
        unit_src = match.group(2)
        unit_des_1 = match.group(3)
        unit_des_2 = match.group(4)
        num_des_1 = int(float(value1) * dict_convert[unit_src, unit_des_1])
        num_des_2 = int(round((float(value1) * dict_convert[unit_src, unit_des_1] - num_des_1) * dict_convert[unit_src, unit_des_2]))
        result_str = str(num_des_1) + " " + unit_des_1 + " " + str(num_des_2) + " " + unit_des_2
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False 
    return found, result_str

def build_dict_convert_time():
    dict_convert = {("giây", "giây"): 1,
                    ("phút", "giây"): 60,
                    ("giờ", "giây"): 60 * 60,
                    ("ngày", "giây"): 24 * 60 * 60,
                    
                    ("giây", "phút"): 1/60,
                    ("phút", "phút"): 1,
                    ("giờ", "phút"): 60,
                    ("ngày", "phút"): 24 * 60,
                    
                    ("giây", "giờ"): 1/(60 * 60),
                    ("phút", "giờ"): 1/60,
                    ("giờ", "giờ"): 1,
                    ("ngày", "giờ"): 24,
                    
                    ("giây", "ngày"): 1/(24 * 60 * 60),
                    ("phút", "ngày"): 1/(24 * 60),
                    ("giờ", "ngày"): 1/24,
                    ("ngày", "ngày"): 1}
    return dict_convert

def rulebase_fill_in_time_case_1(question_str):
    '''
    giây|phút|giờ|ngày
    '''
    #60 60 24
    l_units = ["giây", "phút", "giờ", "ngày"]
    dict_convert = build_dict_convert_time()
    pattern_search = r"\b(\d+\s*(giây|phút|giờ|ngày)\s*\d*\s*(giây|phút|giờ|ngày)\s*=\s*[\.,… _*#]*\s*(giây|phút|giờ|ngày))\b"
    pattern_find_value = r"(\d+)\s*(giây|phút|giờ|ngày)"
    matches = re.findall(pattern_search, question_str)
    result = ""
    found = False
    if matches:
        matches = matches[0]
        math_sentece = matches[0]
        des_unit = matches[-1]
        matches_value = re.findall(pattern_find_value, math_sentece)
        if matches_value and len(matches_value) == 2:
            value__src_0, unit_src_0 = matches_value[0]
            value_src_1, unit__src_1 = matches_value[1]
            result = int(value__src_0) * dict_convert[unit_src_0, des_unit] +\
                     int(value_src_1) * dict_convert[unit__src_1, des_unit]
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if check_valid_matched(math_sentece, question_str):
                found = True 
            else:
                found = False
            
    return found, result

def rulebase_fill_in_time_case_2(question_str):
    '''
    Chia ra làm nhiều case
    
    return the result in string or something else.
    '''
    
    l_units = ["giây", "phút", "giờ", "ngày"]
    dict_convert = build_dict_convert_time()
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(giây|phút|giờ|ngày)\s*=\s*[\.,… _*#]*\s*(giây|phút|giờ|ngày)"
    match = re.search(pattern_search, question_str)
    found = False 
    result = ""
    if match:
        value = match.group(1)
        unit_src = match.group(2)
        unit_des = match.group(3)
        value = str(value).replace(",", ".")
        result = float(value) * dict_convert[unit_src, unit_des] 
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        if check_valid_matched(match.group(1), question_str):
            found = True
        else:
            found = False 
            
    return found, result

def rulebase_fill_in_time_case_4(question_str):
    l_units = ["giây", "phút", "giờ", "ngày"]
    dict_convert = build_dict_convert_time()
    pattern_search = r"(\d+(?:[.,]\d+)?)\s*(giây|phút|giờ|ngày)\s*=\s*[\.,… _*#]*\s*(giây|phút|giờ|ngày)\s*[\.,… _*#]*\s*(giây|phút|giờ|ngày)\b"
    match = re.search(pattern_search, question_str)
    found = False
    result_str = ""
    if match:
        value1 = match.group(1).replace(",", ".")  # Replace comma with dot for decimal values
        unit_src = match.group(2)
        unit_des_1 = match.group(3)
        unit_des_2 = match.group(4)
        num_des_1 = int(float(value1) * dict_convert[unit_src, unit_des_1])
        num_des_2 = int(round((float(value1) * dict_convert[unit_src, unit_des_1] - num_des_1) * dict_convert[unit_src, unit_des_2]))
        result_str = str(num_des_1) + " " + unit_des_1 + " " + str(num_des_2) + " " + unit_des_2
        if check_valid_matched(match.group(1), question_str):
            found = True 
        else:
            found = False 
    return found, result_str

def preprocess_area_unit(question_str):
    dict_convert_unit = {'mm^{2}': "mm2",
                         'cm^{2}': "cm2",
                         'dm^{2}': "dm2",
                         'm^{2}': "m2",
                         'dam^{2}': "dam2",
                         'hm^{2}': "hm2",
                         'ha': "hm2",
                         'km^{2}': "km2"}
    for key in dict_convert_unit.keys():
        question_str = question_str.replace(key, dict_convert_unit[key])
    return question_str

def preprocess_volume_unit(question_str):
    dict_convert_unit = {'mm^{3}': "mm3",
                         'cm^{3}': "cm3",
                         "ml": "cm3",
                         'dm^{3}': "dm3",
                         "l": "dm3",
                         'm^{3}': "m3",
                         'dam^{3}': "dam3",
                         'hm^{4}': "hm3",
                         'ha': "hm3",
                         'km^{3}': "km3"}
    for key in dict_convert_unit.keys():
        question_str = question_str.replace(key, dict_convert_unit[key])
    return question_str

def handle_distance(question_str):
    found, result = rulebase_fill_in_distance_case_1(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_distance_case_4(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_distance_case_3(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_distance_case_2(question_str)
    return found, result

def handle_area(question_str):
    question_str = preprocess_area_unit(question_str)
    found, result = rulebase_fill_in_area_case_1(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_area_case_4(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_area_case_3(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_area_case_2(question_str)
    
    return found, result

def handle_volume(question_str):
    question_str = preprocess_volume_unit(question_str)
    found, result = rulebase_fill_in_volume_case_1(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_volume_case_4(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_volume_case_3(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_volume_case_2(question_str)
    return found, result


def handle_weight(question_str):
    found, result = rulebase_fill_in_weight_case_1(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_weight_case_4(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_weight_case_3(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_volume_case_2(question_str)
    return found, result

def handle_time(question_str):
    found, result = rulebase_fill_in_time_case_1(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_time_case_4(question_str)
    if found:
        return found, result
    found, result = rulebase_fill_in_time_case_2(question_str)
    return found, result

# sample_strings = [
#     "cho caua sau : 1 m - 25 cm = .. .cm",
#     "1m 26cm  = ..,.  cm",
#     "805 m2 = ..,. ha",
#     "5m2 6dm2 = .,… dm2",
#     "66m2 66cm2 = …,. cm2",
#     "12m7dm = … dm.",
#     "12m7dm = … km.",
#     "12m= … dm",
#     "99.15 m  = … dm",
#     "8,12312 cm = ...,. mm",
#     "72km = ...,.. cm",
#     "1m2 25cm2 = ..........,..cm2",
#     "805 m2 = ..,. ha",
#     "5m2 6dm2 = .,… dm2",
#     "66m2 66cm2 = …,. cm2",
#     "18,27 ha = ...km2", 
#     "Số thích hợp điều vào chỗ chấm để 2m^{3} = ……..dm^{3} là:",
#     "Số thích hợp điền vào chỗ chấm 17 tấn 16 kg =............. ...kg là:",
#     "Số thích hợp điền vào chỗ chấm 17 000 kg =............. ...tấn là:",
#     "Số thích hợp điền vào chỗ chấm 17 000 000 ha =............. ...km2 là:",
#     "Số thích hợp điền vào chỗ chấm 170 000cm3 =............. ...m^{3} là:",
#     ""
# ]
if __name__ == "__main__":
    sample_strings = ["Cho 1 giờ 35 phút = … phút”. Số thích hợp để điền vào chỗ chấm là:", "Điền số thích hợp vào chỗ chấm: 3 giờ 10 phút = … phút:"]

    for question_str in sample_strings:
        found_d, result = handle_distance(question_str)
        if found_d:
            print("Distance: ")
            print(question_str)
            print(result)
            print("#######")
        found_a, result = handle_area(question_str)
        if found_a:
            print("Area: ")
            print(question_str)
            print(result)
            print("#######")
            
        found_v, result = handle_volume(question_str)
        if found_v:
            print("Volumne: ")
            print(question_str)
            print(result)
            print("#######")
        found_w, result = handle_weight(question_str)
        if found_w:
            print("Weight: ")
            print(question_str)
            print(result)
            print("#######")
            
        found_t, result = handle_time(question_str)
        if found_t:
            print("Time: ")
            print(question_str)
            print(result)
            print("#######")
            
