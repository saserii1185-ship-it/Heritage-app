import requests
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="سوالف نجد - المساعد التراثي", page_icon="🏜️", layout="centered"
)

st.title("🏜️ سوالف نجد والتراث")
st.write(
    "حيّاك الله يا طويل العمر! أنا مساعدك الذكي، جالس في المجلس وجاهز أعيشك"
    " أجواء نجد العذية وتاريخها وسوالف الأولين."
)

# التحقق من وجود المفتاح في الـ Secrets
if "GEMINI_API_KEY" not in st.secrets:
  st.error(
      "الرجاء إضافة `GEMINI_API_KEY` في قسم الـ Secrets في إعدادات التطبيق."
  )
else:
  token = st.secrets["GEMINI_API_KEY"]

  # رابط الاتصال المباشر المخصص للرمز حقك
  url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
  headers = {
      "Authorization": f"Bearer {token}",
      "Content-Type": "application/json",
  }

  # إدارة سجل المحادثة
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # عرض رسائل الشات السابقة
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # صندوق الإدخال للمستخدم
  if prompt := st.chat_input("تفضل، اسأل عن أي شيء يخص نجد وتراثها..."):
    # إضافة رسالة المستخدم للشات
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
      with st.spinner("جاري صب القهوة والتفكير..."):
        try:
          # دمج التعليمات الشخصية مع سؤال المستخدم مباشرة لضمان السرعة والنجاح
          full_prompt = (
              "تعليمات النظام: أنت مساعد ذكي ابن حلال ومجلس تراثي نجدي، متخصص"
              " بشكل حصري في تاريخ، وتراث، وأمثال، وأعراف، وقصص، ولهجة أهل"
              " نجد العالية. تتحدث بطريقة ودودة جداً، قريبة للقلب، وبروح شبابية"
              " نجدية أصيلة ولطيفة. تستخدم بعض المفردات النجدية المحببة (مثل:"
              " حيّاك الله، يا هلا، سم، أبشر، يامرحباً). سؤال المستخدم هو: "
              + prompt
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
