<div align="center">

# 📄 Resume Parser Web Application

### Automated Bulk Resume Parsing using FastAPI, React & spaCy NLP

<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi"/>
<img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react"/>
<img src="https://img.shields.io/badge/spaCy-NLP-green?style=for-the-badge&logo=spacy"/>
<img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge"/>

</div>

---

# 📌 Overview

This project presents a **Full-Stack Resume Parsing System** designed to automate the recruitment pipeline.  
The system allows users to upload massive batches of resumes and automatically extracts key information into a structured format.

✅ **Bulk ZIP Uploads**  
✅ **Multi-format Support (PDF & DOCX)**  
✅ **Dynamic CSV Export**

The project leverages asynchronous multiprocessing in Python to parse hundreds of resumes in parallel, cutting down hours of manual data entry into mere seconds.

---

# 🎯 Project Objectives

✔ Extract vital candidate details (Name, Email, Phone, Location) from unstructured text  
✔ Handle complex LaTeX PDFs using custom Email-Prefix heuristics  
✔ Prevent CPU bottlenecking using Python's `ProcessPoolExecutor`  
✔ Provide a beautiful, glassmorphism-inspired drag-and-drop React interface  
✔ Easily export parsed results directly to CSV  

---

# 🧠 Core Technologies

## 🔹 Backend (FastAPI + spaCy)
A robust Python backend built from scratch using:
- **FastAPI**: For high-performance async endpoints
- **spaCy & Regex**: For Named Entity Recognition (NER) and pattern matching
- **pdfplumber & python-docx**: For accurate raw text extraction
- **Concurrent Futures**: For parallel processing of multiple files

---

## 🔹 Frontend (React + Vite)
A lightning-fast modern frontend tailored for user experience:
- **Vite & React**: For rapid compilation and component management
- **Tailwind CSS (v3)**: For utility-first, fully responsive styling
- **React Dropzone**: For seamless file and folder drag-and-drop interactions
- **Papaparse**: For instant, client-side CSV generation

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python, JavaScript |
| Backend | FastAPI, Uvicorn |
| Frontend | React, Vite, Tailwind CSS |
| NLP & Parsing | spaCy, pdfplumber, python-docx |
| HTTP & API | Axios |
| Version Control | Git, GitHub |

---

# 🔄 System Workflow

The following pipeline executes when a user drops a batch of resumes:

✅ ZIP Extraction / File Read  
✅ Raw Text Extraction (PDF/DOCX)  
✅ Email & Phone Regex Matching  
✅ Email-Prefix Name Inference Heuristics  
✅ NLP Fallback (spaCy) for Entities  
✅ JSON Response Serialization  
✅ Temporary File Cleanup  

---

# 📊 Extracted Data Points

For every resume processed, the system targets:

- 👤 **Name** (Intelligently filtered against common resume buzzwords)
- 📧 **Email Address**
- 📱 **Phone Number**
- 📍 **Location / GPE**
- 📄 **Original File Name**

---

# 🚀 Future Improvements

🔹 Skills & Technologies Extraction  
🔹 Automated ATS Scoring  
🔹 Direct Integration with PostgreSQL Database  
🔹 Job Description Semantic Matching  
🔹 Real-time WebSockets Progress Bar  

---

---

# ▶️ Installation & Usage

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Gaural193/resume-parser.git
cd resume-parser
```

---

## 2️⃣ Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # (On Windows)
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Start the API Server:
```bash
uvicorn app.main:app --reload
```

---

## 3️⃣ Frontend Setup (React)

Open a new terminal window:
```bash
cd frontend
npm install
```

Start the Vite Development Server:
```bash
npm run dev
```

---

# 📈 Architecture Flow

```text
User Drag-and-Drops ZIP
        ↓
React API Call to FastAPI
        ↓
ZIP Extracted to Temp Directory
        ↓
ProcessPoolExecutor (Parallel Parsing)
        ↓
Regex & spaCy NLP Extraction
        ↓
JSON Array Returned to Frontend
        ↓
User Downloads CSV
```


# 👨‍💻 Author

## Gaural Makwana

🎓 Software Engineer  
🤖 AI, Machine Learning & Full-Stack Enthusiast  

---

<div align="center">

## 🌟 If you like this project, give it a star ⭐

</div>
