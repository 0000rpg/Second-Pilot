from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import uvicorn
import os
from dotenv import load_dotenv
from main import process_chain_request

load_dotenv()

app = FastAPI(title="Task Chain Bot API", description="Backend for LLM task chain processing")

class ChainStep(BaseModel):
    prompt: str
    action: str = Field(..., pattern="^(generate|check|correct|consult)$")
    model: str = "auto"

class ChainRequest(BaseModel):
    chain: List[ChainStep]
    user_id: Optional[str] = "anonymous"
    mode: str = Field("fast", pattern="^(fast|deep|research)$")

class ChainResponse(BaseModel):
    result: str
    history: List[Dict[str, Any]]

@app.post("/process", response_model=ChainResponse)
async def process_chain(request: ChainRequest):
    """
    Принимает цепочку задач, обрабатывает её и возвращает результат.
    """
    input_json = request.model_dump_json()
    output = process_chain_request(input_json)
    if "error" in output:
        raise HTTPException(status_code=400, detail=output["error"])
    return ChainResponse(**output)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)