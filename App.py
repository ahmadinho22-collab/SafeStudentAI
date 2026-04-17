import streamlit as st
import google.generativeai as genai

# إعداد المفتاح
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح مفقود من الإعدادات!")
    st.stop()

# اسم الموديل بالحروف الصغيرة تماماً
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 مساعد الطالب الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف أساعدك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # إرسال الطلب
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
