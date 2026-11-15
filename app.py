import streamlit as st
from google import genai
import json
import os

st.set_page_config(page_title="المكتبة الرقمية للتراث الثقافي", layout="centered")

# الاتصال بالذكاء الاصطناعي باستخدام المفتاح السري المرفوع في الإعدادات
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🏛️ المكتبة الرقمية للتراث الثقافي السعودي")
st.write("منصة ذكاء اصطناعي لاستكشاف وتوثيق التراث الأصيل.")

# قراءة ملف البيانات الخارجي تلقائياً
heritage_context = ""
if os.path.exists("heritage.json"):
    with open("heritage.json", "r", encoding="utf-8") as f:
        heritage_context = f.read()

user_question = st.text_input("🔍 اسأل عن أي موروث ثقافي:")

if user_question:
    with st.spinner("جاري البحث وصياغة الإجابة..."):
        prompt = f"""
        أنت خبير ومرشد ثقافي في المكتبة الرقمية للتراث السعودي.
        أجب عن سؤال المستخدم بأسلوب شيق، دقيق، ومختصر باللغة العربية.
        اعتمد في إجابتك أولاً على هذه البيانات الموثقة إن وجدت: {heritage_context}
        سؤال المستخدم: {user_question}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        st.success("🤖 إجابة المساعد الثقافي:")
        st.write(response.text)
