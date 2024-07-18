# Google-Review-Summarizer

A Flask application which allows users to input specific places to generate summaries of their Google Reviews by using `Gemini AI LLMs`, `Python`, `Flask`, and standard `HTML`, `JS`, `CSS` and `Bootstrap`.

## Key Tech Stack

- `Python 3` for backend logic
- `Flask` for providing a server
- `HTML`, `JavaScript`, and `CSS` for the frontend
- `Bootstrap` for general styling
- `Google Gemini API` as our LLM / AI
- `Pyppeteer` for review scraping
- `Misaka` for rendering `Markdown` in `HTML`
- `thefuzz` for calculating Levenshtein Distance between user input and Google Maps results

## Set-Up

1. Download the required packages via `pip install -r requirements.txt`
2. Generate a Google Gemini AI API key
3. In your `.env` file, set `API_KEY` as your API key
4. Run the `server.py` file and navigate to `http://localhost:5000/` to summarize some reviews!
