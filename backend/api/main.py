# backend/api/main.py

from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
import io
import hashlib
from backend.models.siamese_model import SiameseNetwork
from backend.models.clip_model import clip_model, clip_processor
from backend.utils.image_processing import preprocess_image
from backend.blockchain.blockchain_interaction import register_ip, verify_ip

app = FastAPI()

# Load Siamese Model
siamese_model = SiameseNetwork()
siamese_model.load_state_dict(torch.load("../backend/models/siamese_model.pth"))
siamese_model.eval()

@app.get("/")
def read_root():
    return {"message": "IP Violation Detection API"}

# Image Upload for Detection
@app.post("/detect_violation/")
async def detect_violation(image: UploadFile = File(...)):
    contents = await image.read()
    image = Image.open(io.BytesIO(contents))
    processed_image = preprocess_image(image)
    
    # Compute CLIP Features
    inputs = clip_processor(images=image, return_tensors="pt")
    clip_features = clip_model.get_image_features(**inputs).detach().numpy()

    # Generate perceptual hash (pHash)
    phash_value = hashlib.md5(contents).hexdigest()
    
    # Verify against Blockchain
    verification_result = verify_ip(phash_value)
    if verification_result["owner"]:
        return {"status": "Violation Detected", "owner": verification_result["owner"], "timestamp": verification_result["timestamp"]}
    
    return {"status": "No Violation Detected"}

# Register New Intellectual Property
@app.post("/register_ip/")
async def register_new_ip(image: UploadFile = File(...), sender_address: str, private_key: str):
    contents = await image.read()
    phash_value = hashlib.md5(contents).hexdigest()
    
    tx_hash = register_ip(phash_value, sender_address, private_key)
    return {"message": "Intellectual Property Registered", "tx_hash": tx_hash}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
