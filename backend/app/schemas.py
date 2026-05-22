from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ResumeData(BaseModel):
    file_name: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class ParseResponse(BaseModel):
    status: str
    total_processed: int
    successful: int
    failed: int
    results: List[ResumeData]
    errors: List[str]
