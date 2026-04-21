import os

import streamlit as st
from click import prompt
from openai import OpenAI

# 配置页面基本设置
st.set_page_config(
    page_title="AI智能伴侣",              # 设置浏览器标签页标题
    page_icon="🤖",                       # 设置页面图标（显示在浏览器标签页）
    layout="wide",                        # 设置页面布局为宽屏模式（默认为窄屏）
    initial_sidebar_state="expanded",     # 设置侧边栏初始状态为展开状态
    # 右上角菜单项配置
    menu_items={
        "Get Help": "https://google.com", # 添加"获取帮助"菜单项，点击后跳转到指定URL
    }
)
st.title("🤖 v的智能伴侣")
st.logo("robot.png")
prompt = st.chat_input("请输入你的问题")
# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
if prompt:
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个学习助手，帮助解决python开发学习、就业的问题"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    st.chat_message("assistant").write(response.choices[0].message.content)