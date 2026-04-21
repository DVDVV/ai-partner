import streamlit as st

st.title("标题")
st.write("""Hello, world""")
st.image("img.png")
st.audio("沂蒙颂 (无损音质版) - 王晨、芳华.mp3")
student_data = {
    "name": ["小王","xiaohong","xiaozhang"],
    "age": [18,20,22,24],
    "gender": [18,20,22],
    "hobby": [18,20,22],
    "address": [18,20,220]
}
st.table(student_data)
title = st.text_input("hellotweoweto")
st.write(title)
