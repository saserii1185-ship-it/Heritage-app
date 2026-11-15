import requests
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="المساعد التراثي والثقافي - مدن المملكة",
    page_icon="🏛️",
    layout="centered",
)

st.title("🏛️ موسوعة التراث والثقافة السعودية")
st.write(
    "حيّاك الله! أنا مساعدك الذكي الشامل، جاهز آخذك في رحلة عبر تاريخ وثقافات"
    " وعادات وتقاليد جميع مدن ومناطق المملكة العربية السعودية."
)

# التحقق من وجود المفتاح في الـ Secrets
if "GEMINI_API_KEY" not in st.secrets:
  st.error(
      "الرجاء إضافة `GEMINI_API_KEY` في قسم الـ Secrets في إعدادات التطبيق."
  )
else:
  api_key = st.secrets["GEMINI_API_KEY"]

  # إرسال المفتاح بالطريقة الصحيحة عبر الـ Query Parameter في الرابط
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
  headers = {"Content-Type": "application/json"}

  # إدارة سجل المحادثة
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # عرض رسائل الشات السابقة
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # صندوق الإدخال للمستخدم
  if prompt := st.chat_input(
      "اسأل عن أي مدينة، تراث، عادات، أو تاريخ في المملكة..."
  ):
    # إضافة رسالة المستخدم للشات
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
      with st.spinner("جاري البحث في تراث وتاريخ المدن..."):
        try:
          full_prompt = (
              "أنت مساعد ذكي خبير ومؤرخ متخصص في الثقافة، والتاريخ، والتراث،"
              " والفنون، والعادات، والتقاليد، وأمثال جميع مناطق ومدن المملكة"
              " العربية السعودية. تتحدث بطريقة ودودة، قريبة للقلب، وبروح سعودية"
              " أصيلة ومرحبة. تقدم معلومات دقيقة وغنية عن تراث أي مدينة أو"
              " منطقة يسأل عنها المستخدم. السؤال هو: " + prompt
          )

          payload = {
              "contents": [{
                  "parts": [{"text": full_prompt}]
              }]
          }

          response = requests.post(url, headers=headers, json=payload)

          if response.status_code == 200:
            res_json = response.json()
            answer = res_json["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
          else:
            st.error(
                "عذراً، صار فيه رد من السيرفر: "
                f"{response.status_code} - {response.text}"
            )
        except Exception as e:
          st.error(f"حدث خطأ في الاتصال: {e}")
