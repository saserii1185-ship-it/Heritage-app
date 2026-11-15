from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="المكتبة التراثية الرقمية", page_icon="🏛️", layout="centered"
)

st.title("🏛️ المكتبة التراثية الرقمية")
st.write(
    "مرحباً بك! هذا التطبيق مخصص للإجابة عن كل ما يتعلق بالتراث، التاريخ،"
    " والثقافة."
)

# التحقق من مفتاح الـ API من إعدادات Secrets في ستريمليت
try:
  api_key = st.secrets["GEMINI_API_KEY"]
  client = genai.Client(api_key=api_key)
except Exception:
  st.error(
      "الرجاء إضافة مفتاح `GEMINI_API_KEY` في قسم Secrets في إعدادات ستريمليت."
  )
  st.stop()

# إدارة المحادثة (Chat History)
if "messages" not in st.session_state:
  st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# استقبال إدخال المستخدم
if prompt := st.chat_input("اكتب سؤالك أو استفسارك التراثي هنا..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد بشكل فوري وسريع باستخدام نموذج مستقر
  with st.chat_message("assistant"):
    try:
      response_stream = client.models.generate_content_stream(
          model="gemini-1.5-flash",
          contents=(
              "أنت مساعد ذكي متخصص في التراث والثقافة والتاريخ. أجب عن السؤال"
              f" التالي باحترافية: {prompt}"
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
      st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
