import re
def corrected(text):
    # Remove single characters
    # text = re.sub(r'\b\w\b|@', '', text)
    # Remove single or double characters and '@', excluding specific patterns
    text = re.sub(r'\b(?!1\b|Q2\b|1Q2\b|yv1Qi\b|1Q1\b|1Qi\b|v1\b)\w{1,2}\b|@', '', text)
    # replace misrepresented text with correct text
    text = re.sub(r'.*?(?=Sources)', '', text, flags=re.DOTALL)
    text = re.sub(r'UpaisaO ficial', 'Upaisa Official', text)
    text = re.sub(r'UPaisa', 'Upaisa', text)
    # text = re.sub(r'O ficial', 'Official', text)
    text = re.sub(r'upaisaofficial', 'Upaisa Official', text)
    text = re.sub(r'ufone official', 'Upaisa Official', text)
    text = re.sub(r'ufone_official', 'Upaisa Official', text)
    # ic(text)
    # if "1Q2" in text:
    if any(substring in text for substring in ["1Q2", "1 Q2", "Q2"]):
    # if any(substring in text for substring in ["1Q2", "1 Q2"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Ufone", text)
    elif any(substring in text for substring in ["yv1Qi", "1Q1", "1Qi"]):
        text = re.sub(r"(Sources)(.*)", r"\1 Upaisa", text)
    return text
