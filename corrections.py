import re
from icecream import ic
def corrected_source(text):
    # Remove single or double characters and '@', excluding specific patterns
    text = re.sub(r'\b(?!1\b|Q2\b|1Q2\b|yv1Qi\b|1Q1\b|1Qi\b|v1\b|4G\b)\w{1,2}\b|@', '', text)
    # replace misrepresented text with correct text
    text = re.sub(r'.*?(?=Sources)', '', text, flags=re.DOTALL)
    text = re.sub(r'UpaisaO ficial', 'Upaisa', text)  # Removed 'Official'
    text = re.sub(r'UPaisa', 'Upaisa', text)
    text = re.sub(r'upaisaofficial', 'Upaisa', text)  # Removed 'Official'
    text = re.sub(r'ufone official', 'Ufone', text)  # Removed 'Official'
    text = re.sub(r'ufone_official', 'Ufone', text)  # Removed 'Official'
    text = re.sub(r'4G', "", text)
    text = re.sub('Ufone Corporate', 'Corporate', text)
    # if "1Q2" in text:
    if any(substring in text for substring in ["1Q2", "1 Q2", "Q2"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Ufone", text)
    elif any(substring in text for substring in ["yv1Qi", "1Q1", "1Qi", "1 Q1", "1 Qi", "Qi"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Upaisa", text)
    source_name = re.search(r'Sources\s*(.*)', text).group(1)
    return source_name


def corrected_date_comments(text):
    # Correct date format
    ic(text)
    text = text.replace('Noy', 'Nov')
    match1 = re.search(r'(\w+ \d+, \d+)\n@ Completed Items (\S+)', text)
    if match1:
        date = match1.group(1)  # Extracted date
        completed_items_str = match1.group(2)  # Extracted number of completed items
        # Check if the completed items string is a number
        if completed_items_str.replace(',', '').isdigit():
            return date, completed_items_str
        else:
            return date, None
    # Return None if no match is found
    return None, None

# def corrected_date_of_comments(text):
#     ic(text)
#     # Correct common OCR errors in the date
#     text = text.replace('Noy', 'Nov')
#     # Add more replacements as needed
#     return text

def corrected_date_of_replies(text):
    # Correct date format
    ic(text)
    text = text.replace('Noy', 'Nov')
    match = re.search(r'Activity from (\w+ \d+, \d+)', text)
    date = match.group(1)  # Extracted date    completed_items1 = match1.group(2)  # Extracted number of completed items
    # dict_r = {'Replies Date': date}
    # print(dict_r)
    return date #dict_r

def corrected_time(text):
    # ic(text)
    # Correct time format
    match = re.search(r'((\d+) hours? )?(\d+) minutes?', text)
    if match is not None:
        hours = int(match.group(2)) if match.group(2) else 0
        minutes = int(match.group(3))
        text = hours * 60 + minutes
    else: text = ""
    return text

def corrected_replies(text):
    ic(text)
    match = re.search(r'^[\d,]+', text)
    if match:
        number_str = match.group()
        number_str = number_str.replace(',', '')  # Remove commas
        return int(number_str)  # Convert to integer
    else:
        return None
