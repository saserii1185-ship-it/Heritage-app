from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_title("المساعد الثقافي والتراثي", page_icon="🏛️")

st.title("🏛️ المساعد الثقافي والتراثي")
st.write(
    "مرحباً بك! أنا مساعدك الذكي الجاهز للحديث معك بكل ود ومرونة عن أي معلومة"
    " ثقافية أو تراثية تطلبينها."
)

# التحقق من وجود المفتاح في الـ Secrets
if "GEMINI_API_KEY" not in st.secrets:
  st.warning(
      "الرجاء إضافة `GEMINI_API_KEY` في قسم الـ Secrets في إعدادات التطبيق."
  )
else:
  # تهيئة العميل باستخدام مكتبة قوقل الرسمية
  client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

  # إدارة سجل المحادثة
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # عرض رسائل الشات السابقة
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # صندوق الإدخال للمستخدم
  if prompt := st.chat_input("اكتبي لي أي استفسار ثقافي أو تراثي..."):
    # إضافة رسالة المستخدم للشات
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # توليد الرد من النموذج
    with st.chat_message("assistant"):
      with st.spinner("جاري التفكير..."):
        try:
          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=prompt,
              config={
                  "system_instruction": (
                      "أنت مساعد ذكي متخصص في الثقافة والتراث السعودي (خصوصاً"
                      " التراث النجدي)، تتحدث بطريقة ودودة، قريبة للقلب، وبروح"
                      " شبابية وبسيطة وبكل سلاسة."
                  )
              },
          )
          answer = response.text
          st.markdown(answer)
          st.session_state.messages.append(
              {"role": "assistant", "content": answer}
          )
        except Exception as e:
          st.error(
              "حدث خطأ أثناء الاتصال. (تأكد من صحة مفتاح الـ API في الـ"
              f" Secrets): {e}"
          )
