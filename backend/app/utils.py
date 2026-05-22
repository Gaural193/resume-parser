import os
import shutil
import tempfile
import uuid

def create_temp_dir() -> str:
    """Create a unique temporary directory and return its path."""
    temp_dir = os.path.join(tempfile.gettempdir(), f"resume_parser_{uuid.uuid4().hex}")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def cleanup_temp_dir(temp_dir: str):
    """Remove a temporary directory and all its contents."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
