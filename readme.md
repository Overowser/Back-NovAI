# Novai Backend

This is the backend service for Novai, responsible for scraping novel chapters, preprocessing text, caching results, and serving them to the frontend.

## Features

- Async web scraping (FastAPI-native, Flask-compatible)
- Preprocessing of text for smoother text-to-speech output (e.g., removing visual censorship elements)
- Caching chapters in a local SQLite database
- Serving chapters through API endpoints
- Prepared for future expansions, including scaling the database to more robust solutions (e.g., PostgreSQL)

## Stack

- FastAPI (preferred)
- Flask (optional fallback)
- aiohttp, asyncio (for async scraping)
- SQLite (via aiosqlite)
- Uvicorn or Flask development server

## Setup

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

You can choose to run the backend using **FastAPI** (default) or **Flask** (optional fallback):

### Run FastAPI backend

```bash
uvicorn fastapi_main:app --reload --port 5000
```
Server available at: `http://localhost:5000/`

### Run Flask backend

```bash
python flask_main.py
```
Server also available at: `http://localhost:5000/`

**Note:**  
We keep both FastAPI and Flask running on port 5000 to avoid needing frontend reconfiguration.

## Configuration

- Default database: `novels.db`
- No environment variables are required at this stage.

## Text Preprocessing

Before sending text to the frontend, the backend applies preprocessing to:
- Remove artifacts or symbols (e.g., censorship symbols, replacing "+" with "plus") to optimize clarity for text-to-speech playback

## Python Version

- Developed and tested under **Python 3.12.0**.

## CORS Handling

- CORS is configured in the backend for both FastAPI and Flask servers.  
- This allows the frontend and backend to communicate during development and testing without cross-origin issues.

## Notes

- Future versions may replace SQLite with a more scalable database solution depending on deployment needs.
