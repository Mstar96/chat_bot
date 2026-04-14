import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from openai import OpenAI
from typing import List,Dict
import uuid

load_dotenv("DEEPSEEK_API.env")
#获取环境变量中的API_KEY
API_KEY = os.getenv("DEEPSEEK_API_KEY")
#获取环境变量中的URL
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

app = FastAPI(title = "客户端助手")
clinet = OpenAI(api_key = API_KEY, base_url = BASE_URL)

sessions: Dict[str, List[Dict[str,str]]] = {}

class ChatRequest(BaseModel):
    session_id: str
    messages: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    sid = request.session_id
    if sid not in sessions:
        sessions[sid] = [{
            "role": "system",
            "content": "你是我的人工智能助手，协助我完成各种任务。"
        }]
    sessions[sid].append({
        "role": "user",
        "content": request.messages
    })

    try:
        #调用大模型(不保留对话)
        response = clinet.chat.completions.create(
            model = "deepseek-chat",
            messages = sessions[sid],
            temperature = 0.7,
        )
        reply = response.choices[0].message.content

        sessions[sid].append({"role": "assistant", "content": reply})
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health():
    return {"status": "ok"}
