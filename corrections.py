import re
from icecream import ic
def corrected_source(text):
    # Remove single characters
    # text = re.sub(r'\b\w\b|@', '', text)
    # Remove single or double characters and '@', excluding specific patterns
    text = re.sub(r'\b(?!1\b|Q2\b|1Q2\b|yv1Qi\b|1Q1\b|1Qi\b|v1\b|4G\b)\w{1,2}\b|@', '', text)
    # replace misrepresented text with correct text
    text = re.sub(r'.*?(?=Sources)', '', text, flags=re.DOTALL)
    text = re.sub(r'UpaisaO ficial', 'Upaisa Official', text)
    text = re.sub(r'UPaisa', 'Upaisa', text)
    # text = re.sub(r'O ficial', 'Official', text)
    text = re.sub(r'upaisaofficial', 'Upaisa Official', text)
    text = re.sub(r'ufone official', 'Ufone Official', text)
    text = re.sub(r'ufone_official', 'Ufone Official', text)
    # ic(text)
    # if "1Q2" in text:
    if any(substring in text for substring in ["1Q2", "1 Q2", "Q2"]):
    # if any(substring in text for substring in ["1Q2", "1 Q2"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Ufone", text)
    elif any(substring in text for substring in ["yv1Qi", "1Q1", "1Qi"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Upaisa", text)
    source_name = re.search(r'Sources\s*(.*)', text).group(1)
    return source_name

def corrected_date_comments(text):
    # Correct date format
    match1 = re.search(r'(\w+ \d+, \d+)\n@ Completed Items (\d+)', text)
    date = match1.group(1)  # Extracted date
    completed_items = match1.group(2)  # Extracted number of completed items
    dict_c = {'Date': date, 'Completed Items': completed_items}
    # print(dict_c)
    return dict_c

def corrected_date(text):
    # Correct date format
    match = re.search(r'Activity from (\w+ \d+, \d+)', text)
    date = match.group(1)  # Extracted date    completed_items1 = match1.group(2)  # Extracted number of completed items
    dict_r = {'Date': date}
    # print(dict_r)
    return dict_r

def corrected_time(text):
    # Correct time format
    match = re.search(r'((\d+) hours? )?(\d+) minutes?', text)
    if match is not None:
        hours = int(match.group(2)) if match.group(2) else 0
        minutes = int(match.group(3))
        text = hours * 60 + minutes
    else: text = ""
    ic(text)
    return text