# To do

Left over from the 4 Nov 2026 session. Roughly in priority order.

## Security
- [ ] **Revoke the old Gemini API key.** It was committed in `.env` before `.gitignore` existed and is still in the git history. Delete it in Google AI Studio, create a new one and put it in your local `.env`.

## Bugs
- [ ] **Buttons 2 and 3 send the wrong prompt.** All three buttons use `input_prompt1`, so "Tell me about the resume" and "How can I improve?" return the same percentage match. Switch them to `input_prompt2` and `input_prompt3`.
- [ ] **Scanned or image-only PDFs give no text.** `page.extract_text()` returns an empty string or `None` for them, so Gemini gets an empty resume. Detect this and tell the user, instead of sending the request.
- [ ] **No check for an empty job description.** The app sends the request even when the job description box is blank.

## Cleanup
- [ ] Remove the dead "alternative" `input_pdf_text` lines in `updated_app.py`. Only the `def` line is commented out, so the rest sits inside the real function after its `return`.
- [ ] Remove the commented-out `subprocess` install lines just below the launcher.
- [ ] Decide whether `old_app.py` and `old_reqs.txt` are still needed; delete them or move them to an `archive/` folder.
- [ ] Rename `updated_app.py` to something like `app.py`. Update the README, the launcher's docstring and any hosting settings if you do.
- [ ] Replace `PyPDF2` with `pypdf`, its maintained successor. The API is almost identical: `from pypdf import PdfReader`.

## Environment
- [ ] Rebuild `venv`. It's missing `pyvenv.cfg`, so Python doesn't recognise it as a virtual environment. Delete the folder and run `python3 updated_app.py`, and the launcher recreates it.
- [ ] Point VS Code at the venv (Cmd+Shift+P → **Python: Select Interpreter** → `./venv/bin/python`). That clears the "could not be resolved" import warnings.
- [ ] Pin package versions in `requirements.txt` (e.g. `pip freeze` the working set) so a future release can't break the app.

## Features / hosting
- [ ] Deploy to Streamlit Community Cloud. Leave `GOOGLE_API_KEY` out of its secrets if visitors should bring their own keys.
- [ ] The prompts are written for Data Science / Analytics / ML / AI roles. Make them general, or let the user pick a field.
- [ ] Merge the `fixing-errors` PR into `main` once the bugs above are fixed.
