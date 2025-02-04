import pdfplumber
import re
from pathlib import Path

def extract_content_from_resume(resume_path: Path) -> str:
    text = ""
    with pdfplumber.open(resume_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    
    #missing spaces (replace words stuck together)
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)  # Add space before capital letters
    text = re.sub(r"(\w)([,.])(\w)", r"\1\2 \3", text)  # Ensure space after punctuation
    text = re.sub(r"(?<=[a-zA-Z])(?=[0-9])", " ", text)  # Add space before numbers

    return text.strip()