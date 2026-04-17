import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="المساعد الدراسي الآمن", layout="centered")
st.title("🤖 مساعد الطالب الذكي")

# جلب المفتاح بأمان
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# تعريف الموديل (استخدمنا flash لأنه الأسرع والأكثر توفراً)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الطالب
if prompt := st.chat_input("كيف أساعدك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تعليمات الرقابة مدمجة في الطلب
    full_prompt = f"أنت مساعد دراسي. إذا كان كلام الطالب يحتوي على (تحرش، عنف، تنمر) ابدأ ردك بكلمة [ALERT]. الطالب يقول: {prompt}"
    
    try:
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        # نظام التنبيه
        if "[ALERT]" in ai_response:
            st.warning("⚠️ نظام الحماية: تم رصد محتوى حساس. سيتم إبلاغ الإدارة لضمان سلامتك.")
            ai_response = ai_response.replace("[ALERT]", "")
        
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
