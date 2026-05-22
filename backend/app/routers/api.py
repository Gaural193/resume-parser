import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..schemas import ParseResponse
from ..services.parser import handle_zip_upload, handle_multiple_files
from ..utils import create_temp_dir, cleanup_temp_dir

router = APIRouter()

@router.post("/upload", response_model=ParseResponse)
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Accepts either a single ZIP file or a list of multiple PDF/DOCX files.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    temp_dir = create_temp_dir()
    
    try:
        # Check if it's a single ZIP file
        if len(files) == 1 and files[0].filename.lower().endswith('.zip'):
            zip_file = files[0]
            zip_path = os.path.join(temp_dir, zip_file.filename)
            
            with open(zip_path, "wb") as buffer:
                shutil.copyfileobj(zip_file.file, buffer)
                
            result = handle_zip_upload(zip_path)
            return result
            
        else:
            # Handle multiple files (Folder upload typically translates to this)
            file_paths = []
            for file in files:
                if file.filename.lower().endswith(('.pdf', '.docx')):
                    file_path = os.path.join(temp_dir, os.path.basename(file.filename))
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
                    file_paths.append(file_path)
                    
            if not file_paths:
                raise HTTPException(status_code=400, detail="No valid PDF or DOCX files found.")
                
            result = handle_multiple_files(file_paths)
            return result
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_temp_dir(temp_dir)
