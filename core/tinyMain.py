import torch
import torch.nn as nn
from torch.nn import functional as F
from tinyModel import Ultimatum # Importing the brain you just built
import os
import requests

batch_size = 32      
block_size = 64      
max_iters = 1000     
learning_rate = 1e-3 
device = 'cuda' if torch.cuda.is_available() else 'cpu' 
eval_iters = 200
n_embd = 64          
n_head = 4           
n_layer = 4          
dropout = 0.0        

print(f"[THE ULTIMATUM]")

file_path = 'input.txt'
if not os.path.exists(file_path):
    url = 'https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt'
    data = requests.get(url).text
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

chars = sorted(list(set(data)))
vocab_size = len(chars)
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] 
decode = lambda l: ''.join([itos[i] for i in l])

# 90% Training, 10% Validation
data_tensor = torch.tensor(encode(data), dtype=torch.long)
n = int(0.9*len(data_tensor))
train_data = data_tensor[:n]
val_data = data_tensor[n:]

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

# The Ultimatum Initialisation 
model = Ultimatum(vocab_size, n_embd, block_size, n_head, n_layer, dropout)
m = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

print(f"Model Parameters: {sum(p.numel() for p in m.parameters())/1e6:.2f} Million")

# training
for iter in range(max_iters):
    xb, yb = get_batch('train')

    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

    if iter % 100 == 0:
        print(f"Step {iter}: Loss {loss.item():.4f}")

print(f"Final Loss: {loss.item():.4f}")

# text generation 
print("\n")
context = torch.zeros((1, 1), dtype=torch.long, device=device)
generated_output = decode(m.generate(context, max_new_tokens=500)[0].tolist())
print(generated_output)