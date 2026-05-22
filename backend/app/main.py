from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import api
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume Parser API")

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Resume Parser API is running."}
