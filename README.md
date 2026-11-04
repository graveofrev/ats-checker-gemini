# ats-checker-gemini
A handy app I created that uses Gemini to help create better CVs.

## Setup
1. Get a free Gemini API key at https://aistudio.google.com/apikey
2. Copy `.env.example` to `.env` and paste your key after `GOOGLE_API_KEY=`
3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Run the app:
   ```bash
   python updated_app.py
   ```
   Missing packages from `requirements.txt` are installed automatically on first run, and the app opens in your browser.

Never commit your `.env` file — it holds your personal API key.
