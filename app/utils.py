import re

def clean_text(text):
    # remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # remove email addresses
    text = re.sub(r'\S+@\S+', '', text, flags=re.MULTILINE)
    # remove phone numbers
    text = re.sub(r'\+?\d[\d -]{8,12}\d', '', text)
    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # remove extra whitespace
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    
    return text
