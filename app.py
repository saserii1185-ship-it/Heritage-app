from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="موسوعة التراث النجدي", page_icon="🏜️", layout="centered"
)

st.title("🏜️ موسوعة التراث وثقافة نجد")
st.write(
    "مرحباً بكِ! هذا التطبيق مخصص حصرياً للإجابة عن تراث، تاريخ، عادات، فنون،"
    " وثقافة منطقة نجد العريقة."
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
if prompt := st.chat_input(
    "اكتب استفسارك عن تراث وثقافة نجد (مثل: العرضة، البناء، الملابس التقليدية)..."
):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد بشكل فوري مع تقييد طول النص ليكون سريعاً جداً
  with st.chat_message("assistant"):
    try:
      response_stream = client.models.generate_content_stream(
          model="gemini-3.8-flash",
          contents=(
              "أنت مساعد ذكي وخبير حصرياً في تراث وثقافة نجد. أجب بإيجاز"
              " وتركيز شديد ومباشر عن الكلمة أو السؤال التالي بدون إطالة أو"
              f" تفاصيل مفرطة: {prompt}"
          ),
          config={
              "max_output_tokens": 300
          },  # هذا السطر يجبر النموذج على الاختصار وسرعة الرد
      )


      def stream_generator():
        for chunk in response_stream:
          if hasattr(chunk, "text") and chunk.text:
            yield chunk.text


      full_response = st.write_stream(stream_generator())
      if not full_response:
        full_response = "أهلاً بكِ! تفضلي بطرح سؤالك حول تراث نجد."
      st.session_state.messages.append(
          {"role": "assistant", "content": full_response}
      )

    except Exception as e:
      st.error(f"حدث خطأ أثناء الاتصال: {e}")
