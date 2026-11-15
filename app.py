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
if prompt := st.chat_input("اكتب سؤالك أو استفسارك التراثي هنا..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # توليد الرد باستخدام النموذج الصحيح المخصص لحسابك
  with st.chat_message("assistant"):
    with st.spinner("جاري البحث في الذاكرة التراثية..."):
      try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "أنت مساعد ذكي متخصص في التراث والثقافة والتاريخ. أجب باحترافية"
                f" عن: {prompt}"
            ),
        )
        answer = response.text
        st.markdown(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
      except Exception as e:
        st.error(
            "⚠️ الخوادم تواجه ضغطاً مؤقتاً، جربي إعادة إرسال السؤال بعد ثانية."
        )
