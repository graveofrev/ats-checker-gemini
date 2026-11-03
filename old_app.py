'''
Created by: Revenant [@graveofrev] on 1 Apr 2024

This app is designed to help job seekers improve their resumes and increase their chances of getting past Applicant Tracking Systems (ATS). It allows users to upload their resumes in PDF format and provides insights based on the job description provided.
'''

import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pdf2image
import google.generativeai as genai

## Part 1: Base configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, input):
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content([prompt, input]) # type: ignore
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Converts the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert data from PDF to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()
            }
        ]
                
        return pdf_parts
    else:
        raise FileNotFoundError("No file detected.")
    
## Part 2: Streamlit Application
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format.", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the resume.")

submit2 = st.button("How can I improve?")

submit3 = st.button("Percentage match.")


## Part 3: Prompt Engineering
input_prompt1 = """
You are an experienced Human Resources Manager with experience in the fields of Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Machine Learning and Artificial Intelligence. Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the job description. 
Highlight the strengths and weaknesses of the application in relation to the specified job description.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of the fields of Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Machine Learning and Artificial Intelligence and deep ATS functionality.
Your task is to evaluate the resume against the provided job description and provide a percentage of match, depending on if the resume matches the job description.
Your output should be structured such that first you show the percentage match, then list the keywords missing from the resume, and then, some final thoughts on the resume.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        input_given = f"{'Resume: '} {pdf_content} {'Job Description'} {input_text}"
        response = get_gemini_response(input_prompt1, input_given)
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        input_given = f"{'Resume: '} {pdf_content} {'Job Description'} {input_text}"
        response = get_gemini_response(input_prompt3, input_given)
        st.subheader("Response: ")
        st.write(response)
    else:
        st.write("Please upload the resume.")