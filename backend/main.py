from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Initialisation 
app = FastAPI(title="The Ultimatum API", version="0.1.0")

# Request Structure
class ChatRequest(BaseModel):
    message: str
    model_name: str = "llama3"

# Chat Endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Connect to Ollama
        llm = ChatOllama(model=request.model_name, temperature=0.7)
        
        # Define the persona
        messages = [
            SystemMessage(content="You are The Ultimatum. Answer directly and efficiently."),
            HumanMessage(content=request.message),
        ]
        
        # Get response
        ai_response = llm.invoke(messages)
        return {"response": ai_response.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "The Ultimatum is breathing."}