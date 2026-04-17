import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="المساعد الدراسي الآمن", layout="centered")
st.title("🤖 مساعد الطالب الذكي")

# جلب المفتاح من Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("لم يتم العثور على مفتاح API في الإعدادات.")
    st.stop()

# تعريف الموديل (تأكد من الحروف الصغيرة تماماً)
model = genai.GenerativeModel('gemini-1.5-flash')

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة الطالب
if prompt := st.chat_input("كيف أساعدك في دروسك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الموديل
    try:
        # تعليمات الرقابة مدمجة
        full_prompt = f"أنت مساعد دراسي. إذا كان كلام الطالب يحتوي على (عنف، تنمر، تحرش) ابدأ ردك بـ [ALERT]. الطالب يقول: {prompt}"
        
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        if "[ALERT]" in ai_response:
            st.warning("⚠️ تنبيه أمني: تم رصد محتوى حساس. نحن نهتم بسلامتك.")
            ai_response = ai_response.replace("[ALERT]", "")
        
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
