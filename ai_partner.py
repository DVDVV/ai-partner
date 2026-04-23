import datetime
import os
from datetime import date

import streamlit as st
from openai import OpenAI
from streamlit import session_state
import json

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

#保存会话
def save_session():
    if st.session_state['current_session']:
        # 构建新的会话对象
        session_data = {
            "name": st.session_state['ai_name'],
            "character": st.session_state['ai_character'],
            "current_session": st.session_state['current_session'],
            "messages": st.session_state['message']
        }
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{session_data['current_session']}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
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
if 'message' not in st.session_state:
    st.session_state['message'] = []
if 'ai_character' not in st.session_state:
    st.session_state['ai_character'] = '一个python教师'
# 创建当前会话session
if 'current_session' not in st.session_state:
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    st.session_state['current_session'] = now

#加载所有的会话列表信息
def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        for file in os.listdir("sessions"):
            if file.endswith(".json"):
                with open(f"sessions/{file}", "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                    session_list.append(session_data)
    return session_list
#加载点击的会话信息
def load_session(session_id):
    st.session_state['message'] = []
    if os.path.exists(f"sessions/{session_id}.json"):
        with open(f"sessions/{session_id}.json", "r", encoding="utf-8") as f:
            session_data = json.load(f)
            st.session_state['message'] = session_data['messages']
            st.session_state['name'] = session_data['name']
            st.session_state['character'] = session_data['character']
            st.session_state['current_session'] = session_data['current_session']
            if session_data['messages']:
                st.session_state['message'] = session_data['messages']
                st.write(f"{st.session_state['message']} 的对话记录")
                st.rerun()
#左侧侧边栏
with st.sidebar :
    if st.button("新建会话",width="stretch"):
        #保存当前会话
        save_session()
        if st.session_state['message']:
            #创建一个新会话
            st.session_state['message'] = []
            st.session_state['current_session'] = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_session()
            #重新运行页面
            st.rerun ()
        else:
            st.warning("这已经是新会话了！")
    st.text("历史会话")
    #展示历史会话列表
    for session in load_sessions():
        col1,col2 = st.columns([4,1])
        with col1:
            #点击加载会话信息
            if st.button(label=f"{session['current_session']}",key=f"load_{session['current_session']}",width="stretch",icon="📕"):
                load_session(session['current_session'])
        with col2:
            #点击删除会话
            if st.button(label="",key=f"delete_{session['current_session']}",args=(session['current_session'],),width="stretch",icon="❌"):
                pass
    #点击历史会话显示
    if st.session_state['current_session']:
        #保存当前会话
        save_session()


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
