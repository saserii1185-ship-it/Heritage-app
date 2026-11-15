from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="المساعد الثقافي والتراثي", page_icon="🏛️", layout="centered"
)

st.title("🏛️ المساعد الثقافي والتراثي")
st.write(
    "مرحباً بكِ! أنا مساعدك الذكي الجاهز للحديث معكِ بكل ود ومرونة عن أي"
    " معلومة ثقافية أو تراثية تطلبينها."
)

# التحقق من مفتاح الـ API
try:
  api_key = st.secrets["GEMINI_API_KEY"]
  client = genai.Client(api_key=api_key)
except Exception as e:
  st.error(f"خطأ في إعداد مفتاح الـ API: {e}")
  st.stop()

# إدارة المحادثة (Chat History)
if "messages" not in st.session_state:
  st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# استقبال إدخال المستخدم
if prompt := st.chat_input("اكتبي لي أي استفسار ثقافي أو تراثي..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد بطريقة ودية وطبيعية تماماً مثل المحادثة
  with st.chat_message("assistant"):
    with st.spinner("جاري التفكير..."):
      try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "أنت مساعد ذكي يتحدث بطريقة ودية، طبيعية، ومرنة تماماً مثل"
                " المحادثة البشرية، ومتخصص في تقديم المعلومات الثقافية والتراثية"
                " (مع التركيز على تراث وثقافة نجد وكل ما تطلبه المستخدمة)."
                f" أجب بطريقة جذابة ومباشرة عن: {prompt}"
            ),
        )
        answer = response.text
        st.markdown(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
      except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال: {e}")
