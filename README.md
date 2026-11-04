# ATS Resume Checker (Gemini)

A Streamlit web app that checks your resume against a job description the way an Applicant Tracking System (ATS) might. Upload your resume as a PDF, paste the job description, and Google's Gemini AI tells you how well they match and what to improve.

## Features

- **Percentage match**: an estimate of how closely your resume fits the job description.
- **Resume review**: strengths and weaknesses of your application for the role.
- **Improvement tips**: what to change to get past the ATS.

The prompts are currently written for Data Science, Business Analytics, Machine Learning and AI roles.

## How it works

```
Resume PDF ──> text extracted (PyPDF2) ──> prompt + job description ──> Gemini ──> answer streamed to the page
```

The app reads the text straight from the PDF rather than converting pages to images, which is faster and avoids OCR mistakes. As a result, **scanned or image-only PDFs aren't supported yet**. Your resume needs selectable text.

## Getting started

### Requirements
- Python 3.10 or newer
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Run it locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/graveofrev/ats-checker-gemini.git
   cd ats-checker-gemini
   ```

2. **Add your API key** (optional; you can also paste it into the app)
   ```bash
   cp .env.example .env
   ```
   Open `.env` and put your key after `GOOGLE_API_KEY=`.

3. **Start the app**
   ```bash
   python3 updated_app.py
   ```
   On the first run, the app creates a virtual environment in `venv/`, installs everything from `requirements.txt`, and opens in your browser. Later runs start straight away.

You can still run it the standard Streamlit way:
```bash
pip install -r requirements.txt
streamlit run updated_app.py
```

### Where the app looks for the API key
1. The `GOOGLE_API_KEY` environment variable (this is how hosting platforms provide secrets)
2. A `.env` file in the project folder. Changes apply the next time the page reloads, with no restart needed.
3. If neither has a key, the app asks for one on the page.

> **Never commit your `.env` file.** It contains your personal API key. It's already listed in `.gitignore`.

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `ImportError: cannot import name 'genai' from 'google'` | The `google-genai` package isn't installed in the Python you're using. Run with `python3 updated_app.py` so the launcher sets things up, or `pip install -r requirements.txt` inside your virtual environment. If you have Anaconda, check that `which streamlit` points to your venv, not Anaconda. |
| `error: externally-managed-environment` | Your system Python (e.g. Homebrew's) doesn't allow pip installs. Use `python3 updated_app.py`, which installs into the project's own `venv/` instead. |
| "This API key has used up its free Gemini allowance" | The free tier has a daily request limit per model. Wait for it to reset, use another key, or enable billing in Google AI Studio. |
| "Gemini is getting more requests than it can handle" | Google's servers are temporarily overloaded. Wait a minute and try again. |
| The app doesn't ask for a key | A key was found in your environment or `.env`. To test what visitors see, run `GOOGLE_API_KEY= python3 updated_app.py`. |
| The response is empty or nonsensical | Check that your PDF has selectable text. Scanned resumes aren't supported yet. |

## Project structure

```
updated_app.py     The app: launcher, PDF reading, Gemini calls and the Streamlit interface
requirements.txt   Python packages the app needs
.env.example       Template for your local .env file
old_app.py         Previous version (PDF → image approach), kept for reference
TODO.md            Known issues and planned improvements
```

## Built with

- [Streamlit](https://streamlit.io) for the web interface
- [Google Gen AI SDK](https://github.com/googleapis/python-genai) (`google-genai`) for Gemini
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction
- [python-dotenv](https://pypi.org/project/python-dotenv/) for reading `.env`

## Known issues

See [TODO.md](TODO.md). The main one: the **"Tell me about the resume"** and **"How can I improve?"** buttons currently return the same answer as **"Percentage match"**.

## License

[MIT](LICENSE) © 2024 Revenant ([@graveofrev](https://github.com/graveofrev)).
