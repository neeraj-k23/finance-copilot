from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.services.ingest import ingest_transactions
from backend.services.analytics import (
    get_monthly_spend,
    get_category_breakdown
)

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = ingest_transactions(file_path)
    return result


@router.get("/monthly-spend")
def monthly_spend():
    return get_monthly_spend()


@router.get("/category-breakdown")
def category_breakdown():
    return get_category_breakdown()