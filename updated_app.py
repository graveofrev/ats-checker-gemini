'''
Updated by: Revenant [@graveofrev] on 3 Nov 2026

This app previously used the pdf2image library to convert the PDF to an image and then used the Google Gemini API to analyze the resume. The new version of the app will use a different approach using PyPDF2 to process the PDF and provide insights.

PyPDF2 allows for direct extraction of text from PDF files, which can be more efficient and accurate for analyzing resumes compared to converting them to images. It also ensures better readability and avoids potential issues with image quality or OCR errors.

PDF >> Text >> API >> Response
'''

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() #load all environment variables from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response
def get_gemini_response(prompt):
    response = genai.chat.create(
        model="gemini-pro",
        messages=[
            {"role": "system", "content": "You are an experienced recruitment and HR professional."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.last

def input_pdf_text(pdf_file):
    pdf_reader = pdf.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

'''
Alternative def function:

def input_pdf_text(pdf_file):
    pdf_reader = pdf.PdfReader(pdf_file)
    text = ""
    for page in reader(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text
'''

## Streamlit Application
st.set_page_config(page_title="ATS Resume Expert")
st.header("Let's help you get past the machine!")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Percentage match.")

submit2 = st.button("Tell me about the resume.")

submit3 = st.button("How can I improve?")


## Prompt Template
input_prompt1 = """
You are a well-functioning ATS (Applicant Tracking System) scanner with a deep understanding of the fields of Data Science, Business Analytics, Machine Learning and Artificial Intelligence and well-designed ATS functionality.
Your task is to evaluate the resume against the provided job description and provide a percentage of match, depending on if the resume matches the job description.
"""

input_prompt2 = """
You are a well-functioning ATS (Applicant Tracking System) scanner with a deep understanding of the fields of Data Science, Business Analytics, Machine Learning and Artificial Intelligence.
Your task is to evaluate the resume against the provided job description and provide feedback on how the resume matches the job description.
Your output should be structured such that first you show the percentage match, then list the keywords missing from the resume, and then, some final thoughts on the resume.
"""

input_prompt3 = """
You are an experienced Human Resources Manager with experience in the fields of Data Science, Business Analytics, Machine Learning and Artificial Intelligence. Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the job description. 
Highlight the strengths and weaknesses of the application in relation to the specified job description.
"""

if submit1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}")
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}")
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}")
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume.")