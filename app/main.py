from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import tempfile
import os
import torch
import torch.nn.functional as F
import torchaudio
from model_loader import load_models
from inference import generate_merged_embedding


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")



@app.on_event("startup")
def startup_event():
    load_models()


@app.get("/")
async def index():
    return FileResponse("frontend/index.html", media_type="text/html")


@app.post("/compute_similarity")
async def compute_similarity(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # ---- Save file1 temporarily ----
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp1:
        tmp1.write(await file1.read())
        path1 = tmp1.name

    waveform1, sr1 = torchaudio.load(path1)
    os.remove(path1)

    # ---- Save file2 temporarily ----
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp2:
        tmp2.write(await file2.read())
        path2 = tmp2.name

    waveform2, sr2 = torchaudio.load(path2)
    os.remove(path2)

    # ---- Extract merged embeddings ----
    merged_embedding1 = generate_merged_embedding(waveform1, sr1)  # [1, 2560]
    merged_embedding2 = generate_merged_embedding(waveform2, sr2)  # [1, 2560]

    # ---- Compute cosine similarity ----
    #similarity = F.cosine_similarity(merged_embedding1, merged_embedding2).item()

    # ---- Compute Euclidean similarity ----
    euclidean_similarity = torch.norm(merged_embedding1 - merged_embedding2).item()
    euclidean_similarity = 1 / (1 + euclidean_similarity)  # optional conversion to [0,1] similarity


    return {
        "similarity_score": euclidean_similarity
    }
 
 
@app.get("/")
async def  main():
    if __name__ == '__main__':
        uvicorn.run(app, host='0.0.0.0')