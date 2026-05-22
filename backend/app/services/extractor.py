import re
import spacy
import pdfplumber
import docx
from typing import Dict, Any, Optional

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if not loaded
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Regex patterns
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
# Matches various phone formats e.g. +1 (123) 456-7890, 123-456-7890, etc.
PHONE_REGEX = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'

def extract_text_from_pdf(file_path: str) -> str:
    text = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return "\n".join(text)

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_entities(text: str) -> Dict[str, Optional[str]]:
    doc = nlp(text)
    
    name = None
    location = None
    
    # Simple heuristics: first PERSON entity is often the name
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            # Basic validation to avoid picking up random words
            if len(ent.text.split()) >= 2 and len(ent.text) < 50:
                name = ent.text.strip()
        elif ent.label_ == "GPE" and not location:
            location = ent.text.strip()
            
        if name and location:
            break

    # If spacy failed to find a person, we could optionally try first line of text
    if not name:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Often the first non-empty line is the name
            potential_name = lines[0]
            if 2 <= len(potential_name.split()) <= 4 and len(potential_name) < 50:
                 name = potential_name

    # Extract Email
    email_match = re.search(EMAIL_REGEX, text)
    email = email_match.group(0) if email_match else None

    # Extract Phone
    phone_match = re.search(PHONE_REGEX, text)
    phone = phone_match.group(0) if phone_match else None

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location
    }

def process_file(file_path: str, original_filename: str) -> Dict[str, Any]:
    text = ""
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        text = extract_text_from_docx(file_path)
    
    if not text.strip():
        return {
            "file_name": original_filename,
            "error": "Could not extract text or file is empty"
        }
        
    entities = extract_entities(text)
    return {
        "file_name": original_filename,
        "name": entities["name"],
        "email": entities["email"],
        "phone": entities["phone"],
        "location": entities["location"]
    }
