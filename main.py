import io
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image,ImageDraw
import torch
from torchvision import transforms,models
import cv2
import random

model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

transform = transforms.Compose([
    transforms.ToTensor()
    
])

app = FastAPI()
def predict_and_draw(image:Image.Image):
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        predictions = model(img_tensor)
    prediction = predictions[0]
    boxes = prediction['boxes'].cpu().numpy()
    labels = prediction['labels'].cpu().numpy()
    scores = prediction['scores'].cpu().numpy()
    img_rgb =image.convert("RGB")
    draw = ImageDraw.Draw(img_rgb)
    for box, label, score in zip(boxes, labels, scores):
        if score > 0.7:  # Threshold for displaying boxes
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
           
    return img_rgb
@app.get("/")
def read_root():
    return {"message": "Welcome to the Object Detection API!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Predict and draw bounding boxes
    result_image = predict_and_draw(image)
    
    # Save the result to a BytesIO object
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")