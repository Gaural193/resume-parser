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

# Pre-compile the regex for performance
BAD_WORDS_PATTERN = re.compile(
    r'\b(?:resume|cv|curriculum vitae|app|deep learning|machine learning|data|scientist|'
    r'software|engineer|developer|python|jupyter|notebook|project|github|linkedin|'
    r'education|experience|skills)\b',
    flags=re.IGNORECASE
)

def clean_name(raw_name: str) -> Optional[str]:
    if not raw_name:
        return None
    
    # Use the pre-compiled regex (much faster than a loop)
    clean = BAD_WORDS_PATTERN.sub('', raw_name)
    
    # Remove non-alphabetical characters (keeping spaces)
    clean = re.sub(r'[^a-zA-Z\s]', '', clean)
    # Condense spaces and strip
    clean = ' '.join(clean.split()).strip()
    return clean

def extract_name_from_email_heuristic(email: str, text: str) -> Optional[str]:
    if not email:
        return None
    prefix = email.split('@')[0].lower()
    # Remove numbers from prefix for matching
    prefix = re.sub(r'[0-9]', '', prefix)
    prefix_chars = set(prefix)
    if not prefix_chars:
        return None
        
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    best_line = None
    best_score = 0.0
    
    for line in lines[:15]: # check first 15 lines
        clean_l = clean_name(line)
        if not clean_l:
            continue
        words = clean_l.split()
        if not (1 <= len(words) <= 4):
            continue
            
        line_chars_str = clean_l.lower().replace(" ", "")
        line_chars = set(line_chars_str)
        if not line_chars:
            continue
            
        # Calculate character overlap
        match_count = sum(1 for c in line_chars_str if c in prefix)
        score = match_count / len(line_chars_str)
        
        # If the line strongly matches the email prefix characters
        if score > best_score and score > 0.7: 
            best_score = score
            best_line = clean_l
            
    return best_line

def extract_entities(text: str) -> Dict[str, Optional[str]]:
    doc = nlp(text)
    
    name = None
    location = None
    
    # Extract Email first to use as a heuristic for Name
    email_match = re.search(EMAIL_REGEX, text)
    email = email_match.group(0) if email_match else None

    # Try Email Heuristic first (Highly accurate for resumes)
    name = extract_name_from_email_heuristic(email, text)
    
    # Fallback to Spacy PERSON
    if not name:
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                candidate = clean_name(ent.text)
                if candidate and len(candidate.split()) >= 2 and len(candidate) < 50:
                    name = candidate
                    break

    # Extract Location
    for ent in doc.ents:
        if ent.label_ == "GPE" and not location:
            location = ent.text.strip()
            break

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
