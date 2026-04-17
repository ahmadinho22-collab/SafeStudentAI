import streamlit as st
import google.generativeai as genai
import os

# إعداد مفتاح الـ API من إعدادات الموقع السرية
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="المساعد الدراسي الآمن", layout="centered")
st.title("🤖 مساعد الطالب الذكي")

# تعليمات الرقابة
SYSTEM_PROMPT = "أنت مساعد دراسي. إذا لاحظت أي إشارة لتحرش أو عنف أو تنمر، ابدأ ردك بكلمة [ALERT] ثم ساعد الطالب."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if not message["content"].startswith("[ALERT]"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("كيف أساعدك في دروسك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = model.generate_content(f"{SYSTEM_PROMPT} \n الطالب: {prompt}")
    
    if "[ALERT]" in response.text:
        st.error("⚠️ تنبيه: تم رصد محتوى حساس. سيتم توجيهك للمختصين لحمايتك.")
        full_res = response.text.replace("[ALERT]", "")
    else:
        full_res = response.text

    with st.chat_message("assistant"):
        st.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})
