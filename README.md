# Resume Parser Web Application

A production-ready web application for bulk parsing resumes (PDF & DOCX).

## Features
- Upload ZIP files or folders of resumes.
- Extract Name, Email, Phone, and Location.
- Display results in a responsive data table.
- Download results as CSV.

## Architecture
- **Frontend**: React (Vite) + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Extraction**: `pdfplumber`, `python-docx`, `spacy`, `regex`

## Setup Instructions

### Backend
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Download spaCy model: `python -m spacy download en_core_web_sm`
6. Run the server: `uvicorn app.main:app --reload` (Runs on http://localhost:8000)

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev` (Runs on http://localhost:5173)

## Environment Variables
See `.env.example` for required environment variables.
