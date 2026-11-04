'''
Updated by: Revenant [@graveofrev] on 3 Nov 2026

This app previously used the pdf2image library to convert the PDF to an image and then used the Google Gemini API to analyze the resume. The new version of the app will use a different approach using PyPDF2 to process the PDF and provide insights.

PyPDF2 allows for direct extraction of text from PDF files, which can be more efficient and accurate for analyzing resumes compared to converting them to images. It also ensures better readability and avoids potential issues with image quality or OCR errors.

PDF >> Text >> API >> Response
'''


## Launcher: lets the app start with just `python updated_app.py`
# Streamlit is already imported when it runs this script, so this block only fires on a plain `python` run.
import sys
if "streamlit" not in sys.modules:
    import importlib.util
    import os
    import subprocess

    app_dir = os.path.dirname(os.path.abspath(__file__))

    # System-wide Pythons (e.g. Homebrew) refuse pip installs, so hop over to the project's own venv, creating it if needed
    venv_dir = os.path.join(app_dir, "venv")
    if sys.prefix == sys.base_prefix and os.path.realpath(sys.prefix) != os.path.realpath(venv_dir):
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")
        if not os.path.exists(venv_python):
            print("Creating virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        sys.exit(subprocess.call([venv_python, os.path.abspath(__file__)] + sys.argv[1:]))

    required =["streamlit", "google.genai", "PyPDF2", "dotenv"]
    if any(importlib.util.find_spec(m) is None for m in required):
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(app_dir, "requirements.txt")])

    sys.exit(subprocess.call([sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)] + sys.argv[1:]))


#import subprocess
#import sys
#subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "current_reqs.txt"])

import streamlit as st
#import google.generativeai as genai
from google import genai
from google.genai import errors, types
import httpx
import os
import PyPDF2 as pdf

from dotenv import dotenv_values

# Hosting secrets arrive as environment variables; locally, read .env fresh on every rerun so edits apply without a restart
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
api_key = os.getenv("GOOGLE_API_KEY") or dotenv_values(env_file).get("GOOGLE_API_KEY")

## Gemini Response
# Main model first; the backup takes over if the main one is overloaded or out of quota (each model has its own free daily limit)
MODELS = [
    ("gemini-3.8-flash", types.ThinkingConfig(thinking_level="low")),
    ("gemini-2.5-flash", types.ThinkingConfig(thinking_budget=0)),
]

# Streams the answer piece by piece; low thinking keeps the wait before the first words short
def get_gemini_response(prompt):
    for i, (model, thinking) in enumerate(MODELS):
        started = False
        chunk = None
        try:
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are an experienced recruitment and HR professional.",
                    thinking_config=thinking,
                ),
            ):
                if chunk.text:
                    started = True
                    yield chunk.text
            # Gemini can finish without any text (e.g. a blocked answer), which would otherwise leave the page silently blank
            if not started:
                reason = chunk.candidates[0].finish_reason if chunk and chunk.candidates else "unknown"
                st.warning(f"Gemini sent back an empty answer (reason: {reason}). Please try again.")
            return
        except errors.ServerError:
            if not started and i < len(MODELS) - 1:
                continue
            st.error("Gemini is getting more requests than it can handle right now. Please wait a minute and try again.")
            st.stop()
        except errors.ClientError as e:
            if e.code != 429:
                st.error(f"Gemini request failed ({e.code}): {e.message}. Check that your API key is correct.")
                st.stop()
            if not started and i < len(MODELS) - 1:
                continue
            st.error("This API key has used up its free Gemini allowance for now. Try again later, use a different key, "
                     "or turn on billing at https://aistudio.google.com/apikey. "
                     "Details: https://ai.google.dev/gemini-api/docs/rate-limits")
            st.stop()
        except errors.APIError as e:
            st.error(f"Gemini request failed ({e.code}): {e.message}. Check that your API key is correct and has quota left.")
            st.stop()
        except httpx.TimeoutException:
            st.error("Gemini took too long to respond. It may be busy right now, so please try again in a minute.")
            st.stop()

def input_pdf_text(pdf_file):
    pdf_reader = pdf.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

#Alternative def function:

#def input_pdf_text(pdf_file):
    pdf_reader = pdf.PdfReader(pdf_file)
    text = ""
    for page in reader(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text

## Streamlit Application
st.set_page_config(page_title="ATS Resume Expert")
st.header("Let's help you get past the machine!")

# No key configured on the server, so visitors bring their own (kept only for their session, never stored)
if not api_key:
    st.info("This app uses Google's Gemini AI, so you'll need your own API key to use it. "
            "It's free: sign in at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), "
            "click **Create API key**, and paste it below. It's only used for your session and never saved.")
    api_key = st.text_input("Your Gemini API key", type="password", placeholder="Paste your key here")
    if not api_key:
        st.stop()
# Retries brief overloads and server errors a few times with growing pauses; 429 is left out since quota limits don't clear in seconds
client = genai.Client(
    api_key=api_key,
    # Timeout (ms) turns a hung request into a visible error instead of an endless "Running..."
    http_options=types.HttpOptions(timeout=90_000, retry_options=types.HttpRetryOptions(attempts=3, initial_delay=1, max_delay=8, http_status_codes=[408, 500, 502, 503, 504])),
)
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
        st.subheader("Response: ")
        st.write_stream(get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}"))
    else:
        st.write("Please upload the resume.")

elif submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        st.subheader("Response: ")
        st.write_stream(get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}"))
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        st.subheader("Response: ")
        st.write_stream(get_gemini_response(input_prompt1 + f"\n\nResume: {text}\n\nJob Description: {input_text}"))
    else:
        st.write("Please upload the resume.")