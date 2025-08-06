from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from utils.extract_text import extract_text_from_pdf
from classifier import classify_text_zero_shot
from utils.file_handler import move_file_to_category
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    temp_path = os.path.join(TEMP_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print("file saved temporarily at:", temp_path)
        text = extract_text_from_pdf(temp_path)
        print("Extracted text:", text[:1000])  # Print first 1000 characters for debugging
        predicted_label = classify_text_zero_shot(text)
        print("Predicted label:", predicted_label)
        # return {"message":"Text extraction completed"}

    #     # Move file to the appropriate folder
        final_path = move_file_to_category(temp_path, predicted_label, UPLOAD_DIR)
        return {"message": "File classified and moved successfully.", "label": predicted_label, "path": final_path}
        # return {"message": "Test completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list-files/{category}")
def list_files(category: str):
    category_path = os.path.join(UPLOAD_DIR, category)
    if not os.path.exists(category_path):
        return {"files": []}

    files = os.listdir(category_path)
    return {"files": files}