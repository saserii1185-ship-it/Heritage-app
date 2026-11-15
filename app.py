import time
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

  # توليد الرد مع نظام إعادة المحاولة التلقائية للتعامل مع ضغط الخوادم (503)
  with st.chat_message("assistant"):
    success = False
    full_response = ""

    for attempt in range(3):
      try:
        response_stream = client.models.generate_content_stream(
            model="gemini-3.8-flash",
            contents=(
                "أنت مساعد ذكي وخبير حصرياً في تراث وثقافة وتاريخ وعادات منطقة"
                " نجد في المملكة العربية السعودية. أجب باحترافية وتفصيل عن السؤال"
                f" التالي ضمن هذا النطاق: {prompt}"
            ),
        )


        def stream_generator():
          for chunk in response_stream:
            if hasattr(chunk, "text") and chunk.text:
              yield chunk.text


        full_response = st.write_stream(stream_generator())
        success = True
        break
      except Exception as e:
        # إذا كان الخطأ بسبب الضغط (503)، نحاول مرة أخرى تلقائياً
        if ("503" in str(e) or "UNAVAILABLE" in str(e)) and attempt < 2:
          time.sleep(1)
          continue
        else:
          success = False
          break

    if success and full_response:
      st.session_state.messages.append(
          {"role": "assistant", "content": full_response}
      )
    else:
      error_msg = (
          "⚠️ الخوادم تواجه ضغطاً مؤقتاً الآن (خطأ 503). يرجى إعادة إرسال"
          " السؤال بعد ثوانٍ قليلة وسيعمل فوراً."
      )
      st.error(error_msg)
      st.session_state.messages.append(
          {"role": "assistant", "content": error_msg}
      )
