from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
# from backend import get_text
from backend_async import get_text

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can specify specific domains instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class RequestData(BaseModel):
    keyword: str
    chapter: int
    number: int

@app.post("/api/")
async def get_user(req: RequestData):
    user_data = await get_text(req.keyword, req.chapter, req.number)
    return user_data

# To run:
# uvicorn your_file_name:app --reload
