import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title = "智能客服助手")
st.title("🤖 智能客服助手")

#初始化聊天内容
if "messages" not in st.session_state:
    st.session_state.messages = []
#显示历史信息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#输入框
if prompt := st.chat_input("请输入你的问题"):
    #显示用户信息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

#调用后端API
    with st.chat_message("assistant"):
        with st.spinner("思考中"):
            try:
                response = requests.post(API_URL, json={"messages": prompt})
                if response.status_code == 200:
                    reply = response.json()["reply"]
                else:
                    reply = f"错误:{response.status_code}"
            except Exception as e:
                reply = f"连接后端失败：{str(e)}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})