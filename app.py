import datetime
import os

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from google import genai
from google.genai import types

## Part 1: Base configuration
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_PDF_MB = 5
# Limits keep a public demo from using up the owner's API quota
MAX_RUNS_PER_SESSION = 10
MAX_RUNS_PER_DAY = 100


def get_setting(name, default=None):
    # Streamlit Community Cloud provides secrets via st.secrets; locally we fall back to .env
    try:
        if name in st.secrets:
            return st.secrets[name]
    except FileNotFoundError:
        pass
    return os.getenv(name, default)


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


@st.cache_resource
def get_daily_usage():
    # Shared by every visitor of this app instance
    return {"date": None, "runs": 0}


def check_and_count_run():
    today = datetime.date.today()
    usage = get_daily_usage()
    if usage["date"] != today:
        usage["date"], usage["runs"] = today, 0
    session_runs = st.session_state.get("runs", 0)

    if session_runs >= int(get_setting("MAX_RUNS_PER_SESSION", MAX_RUNS_PER_SESSION)):
        return "You've reached the limit for this session. Please come back later."
    if usage["runs"] >= int(get_setting("MAX_RUNS_PER_DAY", MAX_RUNS_PER_DAY)):
        return "The demo has reached its daily limit. Please try again tomorrow."

    st.session_state["runs"] = session_runs + 1
    usage["runs"] += 1
    return None


def get_gemini_response(prompt, pdf_bytes, job_description):
    client = get_client(get_setting("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=get_setting("GEMINI_MODEL", DEFAULT_MODEL),
        contents=[
            prompt,
            # The whole PDF is sent as a document, so every page is read
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            f"Job description:\n{job_description}",
        ],
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text


## Part 2: Streamlit Application
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

if not get_setting("GOOGLE_API_KEY"):
    st.error("No API key found. Add GOOGLE_API_KEY to a .env file (see .env.example) or to your Streamlit secrets.")
    st.stop()

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

input_prompt2 = """
You are an experienced career coach and resume writer. Review the provided resume against the job description.
Suggest specific improvements: skills worth highlighting, bullet points to reword so they match the role, and gaps to address.
Only rephrase or reorganise experience that is already in the resume. Never invent skills, roles or achievements the candidate does not have.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of the fields of Data Science, Full-Stack Web Development, Big Data Engineering, DevOps, Machine Learning and Artificial Intelligence and deep ATS functionality.
Your task is to evaluate the resume against the provided job description and provide a percentage of match, depending on if the resume matches the job description.
Your output should be structured such that first you show the percentage match, then list the keywords missing from the resume, and then, some final thoughts on the resume.
"""

if submit1:
    selected_prompt = input_prompt1
elif submit2:
    selected_prompt = input_prompt2
elif submit3:
    selected_prompt = input_prompt3
else:
    selected_prompt = None

if selected_prompt:
    if uploaded_file is None:
        st.write("Please upload the resume.")
    elif not input_text.strip():
        st.write("Please paste the job description.")
    elif uploaded_file.size > MAX_PDF_MB * 1024 * 1024:
        st.write(f"Please upload a PDF smaller than {MAX_PDF_MB} MB.")
    elif limit_message := check_and_count_run():
        st.write(limit_message)
    else:
        with st.spinner("Reading your resume..."):
            response = get_gemini_response(selected_prompt, uploaded_file.getvalue(), input_text)
        st.subheader("Response: ")
        st.write(response)
