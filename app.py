from google import genai
import streamlit as st

# إعدادات صفحة ستريمليت
st.set_page_config(
    page_title="سوالف نجد - المساعد التراثي", page_icon="🏜️", layout="centered"
)

st.title("🏜️ سوالف نجد والتراث")
st.write(
    "حيّاك الله يا طويل العمر! أنا مساعدك الذكي، جالس في المجلس وجاهز أعيشك"
    " أجواء نجد العذية، وتاريخها، وسوالف الأولين، وكل ما يطري على بالك عن تراثنا"
    " الأصيل."
)

# التحقق من وجود المفتاح في الـ Secrets
if "GEMINI_API_KEY" not in st.secrets:
  st.error(
      "الرجاء إضافة `GEMINI_API_KEY` في قسم الـ Secrets في إعدادات التطبيق."
  )
else:
  try:
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
    if prompt := st.chat_input("تفضل، اسأل عن أي شيء يخص نجد وتراثها..."):
      # إضافة رسالة المستخدم للشات
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.markdown(prompt)

      # توليد الرد من النموذج بنكهة نجدية خالصة
      with st.chat_message("assistant"):
        with st.spinner("جاري صب القهوة والتفكير..."):
          try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "system_instruction": (
                        "أنت مساعد ذكي ابن حلال ومجلس تراثي نجدي، متخصص بشكل"
                        " حصري في تاريخ، وتراث، وأمثال، وأعراف، وقصص، ولهجة"
                        " أهل نجد العالية. تتحدث بطريقة ودودة جداً، قريبة"
                        " للقلب، وبروح شبابية نجدية أصيلة ولطيفة. تستخدم بعض"
                        " المفردات النجدية المحببة (مثل: حيّاك الله، يا هلا، سم،"
                        " أبشر، يامرحباً) في كلامك بطريقة طبيعية وسلسة، وتجعل"
                        " إجاباتك مليئة بعبق التراث النجدي."
                    )
                },
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
          except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالنموذج: {e}")

  except Exception as e:
    st.error(f"حدث خطأ في تهيئة الاتصال: {e}")
