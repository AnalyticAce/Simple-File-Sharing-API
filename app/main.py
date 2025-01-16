from fastapi import APIRouter, File, Request, UploadFile, FastAPI, HTTPException
import os
import base64
import random
from fastapi.responses import FileResponse
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
file_router = APIRouter(
        prefix="/file",
        tags=["File Management"],
        responses={404: {"description": "Not found"}},
)

FILES_DIR = "files"
METADATA_FILE = os.path.join(FILES_DIR, "metadata.json")

os.makedirs(FILES_DIR, exist_ok=True)

if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        file_metadata = json.load(f)
else:
    file_metadata = {}

templates = Jinja2Templates(directory="templates")

def filesizeformat(value):
    value = float(value)
    if value < 1024:
        return f"{value:.1f} B"
    elif value < 1024*1024:
        return f"{value/1024:.1f} KB"
    else:
        return f"{value/1024/1024:.1f} MB"

templates.env.filters["filesizeformat"] = filesizeformat

@app.get("/")
async def home(request: Request):
    files_data = list(file_metadata.values())
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": files_data,
            "message": None,
            "error": False
        }
    )

@app.get("/download/{file_id}")
async def download_page(request: Request, file_id: str):
    # Check if file exists in metadata
    if file_id not in file_metadata:
        return templates.TemplateResponse(
            "download.html",
            {
                "request": request,
                "file_id": file_id,
                "error": "File not found"
            }
        )
    
    return templates.TemplateResponse(
        "download.html",
        {
            "request": request,
            "file_id": file_id,
            "error": None
        }
    )

def save_metadata():
    with open(METADATA_FILE, "w") as f:
        json.dump(file_metadata, f)

def generate_file_id(file_name):
    return base64.b64encode(file_name.encode()).decode().strip("=") + random.choice("abcdefghijklmnopqrstuvwxyz")

@file_router.post("/upload/")
def upload_file(request: Request, file: UploadFile = File(...)):
    file_id = generate_file_id(file.filename)
    file_path = os.path.join(FILES_DIR, file_id)

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    api_download_url = f"{request.base_url}download/{file_id}"
    download_page_url = f"{request.base_url}download/{file_id}"
    
    file_metadata[file_id] = {
        "original_name": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "download_count": 0,
        "download_page": api_download_url,
        "download_link": download_page_url
    }
    
    save_metadata()
    
    return {
        "file_id": file_id,
        "original_name": file.filename,
        "content_type": file.content_type,
        "download_link": api_download_url,
        "download_page": download_page_url,
        "file_size": len(content),
    }

@file_router.get("/download/{file_id}")
def download_file(file_id: str):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = os.path.join(FILES_DIR, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    metadata = file_metadata[file_id]

    file_metadata[file_id]["download_count"] += 1
    
    save_metadata()
    return FileResponse(
        file_path,
        media_type=metadata["content_type"],
        filename=metadata["original_name"]
    )

@file_router.get("/metadata/")
def get_metadata():
    with open(METADATA_FILE, "r") as f:
        return json.load(f)

@file_router.get("/metadata/{file_id}")
def get_metadata(file_id: str):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file_metadata[file_id]

app.include_router(file_router)
