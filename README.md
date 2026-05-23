# Quote Generator (Flask + SQLite)

A full-stack Quote Generator that:
- Fetches random quotes from **Quotable**
- Saves every generated quote into **SQLite**
- Shows quote history without page reloads (uses `fetch()`)

## Project Structure
```
quote-generator/
  app.py
  requirements.txt
  templates/
    index.html
  static/
    style.css
    script.js
  database.db            # auto-created on first run
```

## Setup & Run

### 1) Install dependencies
From the project folder:

```bash
pip install -r requirements.txt
```

### 2) Start the server
```bash
python app.py
```

### 3) Open in your browser
Go to:
- http://127.0.0.1:5000/

## API Endpoints

### `GET /quote`
- Fetches a random quote from `https://api.quotable.io/random`
- Stores it in SQLite table `quote_history`
- Returns JSON:
```json
{
  "quote": "...",
  "author": "...",
  "created_at": "..."
}
```

### `GET /history`
Returns latest saved quotes (latest first):
```json
{
  "history": [
    {"id": 1, "quote": "...", "author": "...", "created_at": "..."}
  ]
}
```

## Notes
- The app creates `database.db` automatically.
- History is capped at the latest 50 items.

