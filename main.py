from fastapi import FastAPI, File, UploadFile
from lavis.models import load_model_and_preprocess
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import torch
import time
from pydantic import BaseModel
import base64
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading model...")
s_time = time.time()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
tot_time = time.time() - s_time
print(f"Model Loaded in {tot_time}s")

@app.get("/")
def read_root():
    return "Image Captioner API is alive"

@app.post("/")
def read_file(image: bytes = File()):
    raw_image = Image.open(BytesIO(image)).convert("RGB")
    print("Processing caption...")
    s_time = time.time()
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    caption, = model.generate({"image": image})
    tot_time = time.time() - s_time
    print(f"Caption processed in {round(tot_time, 2)}s")
    print(f"caption: {caption}")

    return { "caption": caption }

class CaptionRequest(BaseModel):
    base64: str

class CaptionResponse(BaseModel):
    caption: str

@app.post("/base64")
def caption_base64(body: CaptionRequest):
    image = body.base64
    if ',' in image:
        image = image.split(',')[1]
    
    image = base64.b64decode(image)
    raw_image = Image.open(BytesIO(image)).convert("RGB")
    print("Processing caption...")
    s_time = time.time()
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    caption, = model.generate({"image": image})
    tot_time = time.time() - s_time
    print(f"Caption processed in {round(tot_time, 2)}s")
    print(f"caption: {caption}")

    return { "caption": caption }
