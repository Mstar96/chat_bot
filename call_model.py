import os
from dotenv import load_dotenv
from openai import OpenAI

#任务1：完成调用大模型ai并打印回复的功能
#加载.env中的环境变量
load_dotenv("DEEPSEEK_API.env")
#获取环境变量中的API_KEY
API_KEY = os.getenv("DEEPSEEK_API_KEY")
#获取环境变量中的URL
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
#初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
#调用模型
response = client.chat.completions.create(
    model = "deepseek-chat",
    messages = [
        {"role": "system", "content": "你是我的人工智能助手，协助我完成各种任务。"},
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    temperature = 0.7,
)
#打印回复
print(response.choices[0].message.content)