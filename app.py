from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="المساعد الذكي الشامل", page_icon="🤖", layout="centered"
)

st.title("🤖 المساعد الذكي الشامل")
st.write(
    "مرحباً بك! أنا مساعدك الذكي الجاهز للإجابة عن أي سؤال، نقاش، أو استفسار في"
    " شتى المجالات."
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
if prompt := st.chat_input("اكتب أي شيء في بالك..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد بشكل فوري وسريع لجميع الأسئلة
  with st.chat_message("assistant"):
    try:
      response_stream = client.models.generate_content_stream(
          model="gemini-3.8-flash",
          contents=(
              "أنت مساعد ذكي متعدد الاستخدامات، ودود ومفيد، تجيب على أي سؤال"
              f" أو طلب يطرحه المستخدم باحترافية وسلاسة: {prompt}"
          ),
      )


      # دالة لعرض الكلمات فور توليدها
      def stream_generator():
        for chunk in response_stream:
          if chunk.text:
            yield chunk.text


      # عرض الرد وتخزين النص الكامل تلقائياً
      full_response = st.write_stream(stream_generator())
      st.session_state.messages.append(
          {"role": "assistant", "content": full_response}
      )

    except Exception as e:
      st.error(f"حدث خطأ أثناء الاتصال: {e}")
