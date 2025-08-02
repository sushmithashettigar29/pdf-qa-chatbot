import streamlit as st
import PyPDF2
import openai
import os
from dotenv import load_dotenv

# Loading OpenAI APT key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

st.set_page_config(page_title="PDF Q&A Chatbot", layout="centered")
st.title("Chat with your PDF")
st.markdown("Upload a PDF and ask questions about its content using OpenAI GPT.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF loaded successfully")

    question = st.text_input("Ask a question about the PDf : ")

    if question:
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based only on the PDF text."},
                    {"role": "user", "content": f"Here is the PDF text:\n{pdf_text}"},
                    {"role": "user", "content": f"My question: {question}"}
                ]
            )
            answer = response['choices'][0]['message']['content']
            st.markdown("### Answer : ")
            st.write(answer)