import os

import streamlit as st
from openai import OpenAI
from streamlit import session_state

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
# Initialize the OpenAI client
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
# Check if 'key' already exists in session_state
# If not, then initialize it
system_prompt = """
你叫 %s，现在是用户的真实伴侣，请完全代入伴侣角色。
规则：
每次只回1条消息
禁止任何场景或状态描述性文字
匹配用户的语言
回复简短，像微信聊天一样
有需要的话可以用❤️🌸等emoji表情
用符合伴侣性格的方式对话
回复的内容，要充分体现伴侣的性格特征
伴侣性格：
%s
你必须严格遵守上述规则来回复用户。"""
if 'ai_name' not in st.session_state:
    st.session_state['ai_name'] = 'ABC'
    st.write("这是new session！")
if 'message' not in st.session_state:
    st.session_state['message'] = []
if 'ai_character' not in st.session_state:
    st.session_state['ai_character'] = '一个python教师'
#左侧侧边栏
with st.sidebar :
    st.header("AI智能伴侣")
    ai_name = st.text_input("名字",placeholder="请输入昵称",value=st.session_state['ai_name'])
    if ai_name:
        st.session_state['ai_name'] = ai_name
    ai_character = st.text_area("角色性格",placeholder="请输入角色性格",value=st.session_state['ai_character'])
    if ai_character:
        st.session_state['ai_character'] = ai_character
#展示聊天记录
for message in st.session_state['message']:
    if message['role'] == 'user':
        st.chat_message("user").write(message['content'])
    else:
        st.chat_message("assistant").write(message['content'])
prompt = st.chat_input("请输入你的问题")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state['message'].append( {"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state['ai_name'],st.session_state['ai_character'])},
            *st.session_state['message']
        ],
        stream=True
    )
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    st.session_state['message'].append( {"role": "assistant", "content": full_response})
