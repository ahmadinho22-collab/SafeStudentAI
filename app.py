import streamlit as st
import google.generativeai as genai

# اختبار وجود المفتاح في الإعدادات
if "GEMINI_API_KEY" not in st.secrets:
    st.error("خطأ: مفتاح الـ API غير موجود في إعدادات Secrets!")
    st.stop()

# إعداد المفتاح
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# محاولة تعريف الموديل
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"فشل في إعداد الموديل: {e}")

st.set_page_config(page_title="المساعد الدراسي الآمن", layout="centered")
st.title("🤖 مساعد الطالب الذكي")

SYSTEM_PROMPT = "أنت مساعد دراسي. إذا لاحظت تحرش أو عنف، ابدأ بكلمة [ALERT]."

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
        # محاولة إرسال الرسالة وجلب الرد
        response = model.generate_content(f"{SYSTEM_PROMPT} \n الطالب: {prompt}")
        full_res = response.text
        
        if "[ALERT]" in full_res:
            st.error("⚠️ تم رصد محتوى حساس..")
            full_res = full_res.replace("[ALERT]", "")

        with st.chat_message("assistant"):
            st.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بجوجل: {e}")
        st.info("تأكد أن مفتاح الـ API صحيح ومفعل من Google AI Studio.")
