from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from shared.analyzer import LumenSenseAnalyzer

# 1. Initialize the App
app = FastAPI(title="LumenSense API", description="Psychological Intelligence for AI")

# 2. Define the expected input (Pydantic makes sure the user sends the right data)
class ChatRequest(BaseModel):
    chat_log: str

# 3. Instantiate our Chef
analyzer = LumenSenseAnalyzer()

# 4. Define the Route
@app.post("/api/analyze")
async def analyze_chat(request: ChatRequest):
    if not request.chat_log.strip():
        raise HTTPException(status_code=400, detail="chat_log cannot be empty")
    
    try:
        # Pass the data to the Chef
        result = analyzer.analyze(request.chat_log)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))