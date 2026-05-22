import os
import zipfile
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Any
from .extractor import process_file
from ..utils import create_temp_dir

def extract_zip(zip_path: str, extract_to: str) -> List[str]:
    """Extracts a zip file and returns a list of file paths."""
    extracted_files = []
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            
        for root, _, files in os.walk(extract_to):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx')):
                    extracted_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error extracting ZIP: {e}")
    return extracted_files

def process_files_concurrently(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Process a list of files concurrently using ProcessPoolExecutor."""
    results = []
    
    # ProcessPoolExecutor is better for CPU-bound tasks like parsing/NLP
    # Limit max_workers to avoid overloading memory if many large PDFs
    with ProcessPoolExecutor(max_workers=4) as executor:
        # submit tasks
        futures = []
        for file_path in file_paths:
            original_filename = os.path.basename(file_path)
            futures.append(executor.submit(process_file, file_path, original_filename))
            
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                # Capture unhandled exception during processing
                results.append({
                    "file_name": "unknown",
                    "error": str(e)
                })
                
    return results

def handle_zip_upload(zip_file_path: str) -> Dict[str, Any]:
    """Main pipeline for ZIP uploads."""
    temp_extract_dir = create_temp_dir()
    
    try:
        # 1. Extract ZIP
        files_to_process = extract_zip(zip_file_path, temp_extract_dir)
        
        # 2. Process
        raw_results = process_files_concurrently(files_to_process)
        
        # 3. Format response
        successful = [r for r in raw_results if "error" not in r]
        errors = [f"{r.get('file_name', 'Unknown')}: {r['error']}" for r in raw_results if "error" in r]
        
        return {
            "status": "success",
            "total_processed": len(raw_results),
            "successful": len(successful),
            "failed": len(errors),
            "results": successful,
            "errors": errors
        }
    finally:
         # Clean up is handled by caller or utils
         pass

def handle_multiple_files(file_paths: List[str]) -> Dict[str, Any]:
    """Main pipeline for multiple direct file uploads."""
    raw_results = process_files_concurrently(file_paths)
    
    successful = [r for r in raw_results if "error" not in r]
    errors = [f"{r.get('file_name', 'Unknown')}: {r['error']}" for r in raw_results if "error" in r]
    
    return {
        "status": "success",
        "total_processed": len(raw_results),
        "successful": len(successful),
        "failed": len(errors),
        "results": successful,
        "errors": errors
    }
