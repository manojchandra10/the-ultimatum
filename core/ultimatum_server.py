import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from tinyModel import Ultimatum 
from fastapi.middleware.cors import CORSMiddleware
import os

#config
device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = "ultimatum_model.pt"

# initialise app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


vocab_size = 65 
n_embd = 64
block_size = 64
n_head = 4
n_layer = 4
dropout = 0.0


model = Ultimatum(vocab_size, n_embd, block_size, n_head, n_layer, dropout)

if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
else:
    print("CRITICAL WARNING: Model file not found. Please run tinyMain.py first.")

# helper functions
chars = sorted(list(set(" \n!$&',-.3:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")))
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi.get(c, 0) for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(req: GenerateRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is empty")
    
    context_idx = torch.tensor([encode(req.prompt)], dtype=torch.long, device=device)
    generated_idx = model.generate(context_idx, max_new_tokens=200)
    result_text = decode(generated_idx[0].tolist())
    
    return {"output": result_text}