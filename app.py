import os
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from openai import OpenAI

load_dotenv("DEEPSEEK_API.env")
#获取环境变量中的API_KEY
API_KEY = os.getenv("DEEPSEEK_API_KEY")
#获取环境变量中的URL
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

app = FastAPI(title = "客户端助手")
clinet = OpenAI(api_key = API_KEY, base_url = BASE_URL)

class ChatRequest(BaseModel):
    messages: str
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        #调用大模型(不保留对话)
        response = clinet.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": "你是我的人工智能助手，协助我完成各种任务。"},
                {"role": "user", "content": request.messages}
            ],
            temperature = 0.7,
        )
        reply = response.choices[0].message.content
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health():
    return {"status": "ok"}
