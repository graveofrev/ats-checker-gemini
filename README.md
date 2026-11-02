# ats-checker-gemini
A handy app I created that uses Gemini to help create better CVs.

## Run it locally

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.env.example` to `.env` and paste your key in. `.env` is git-ignored, so the key stays on your machine.
3. Install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Create an app from this repo with `app.py` as the main file, and add your key under **Advanced settings → Secrets**:

```toml
GOOGLE_API_KEY = "your-key-here"
```
