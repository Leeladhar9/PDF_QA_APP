#pip install pdfplumber
#pip install openai==0.28
import streamlit as st
import pdfplumber
import openai

openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def answer_question(pdf_text, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"The following is the text from a PDF document:\n\n{pdf_text}\n\nAnswer the question based on the context: {question}"}
            ],
            max_tokens=200,
            temperature=0.8
        )
        refined_answer = response['choices'][0]['message']['content'].strip()
        return refined_answer
    except Exception as e:
        return f"Error occurred: {str(e)}"

st.title("PDF Question Answering App")

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf is not None:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.write("**PDF Content Extracted Successfully!**")
    question = st.text_input("Ask a question about the uploaded PDF:")
    
    if st.button("Get Answer"):
        if question:
            answer = answer_question(pdf_text, question)
            st.write(f"**Answer:** {answer}")
        else:
            st.write("Please enter a question!")
