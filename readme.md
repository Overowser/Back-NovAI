# NovAI Backend

This repository contains the backend code for the NovAI Novel Reader Application, responsible for scraping novel content, processing text, and serving data to the frontend application.

## Overview

The NovAI backend uses FastAPI to create a web API that scrapes novel content from online sources. It features:

- Asynchronous web scraping with aiohttp and BeautifulSoup
- SQLite database caching for improved performance (prepared for future expansions, including scaling to PostgreSQL)
- Text preprocessing to enhance readability and optimize text-to-speech playback (e.g., removing visual censorship elements)
- RESTful API endpoints for frontend integration

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs (preferred)
- **Flask**: Optional fallback for the backend
- **aiohttp**: Asynchronous HTTP client/server for Python
- **BeautifulSoup4**: HTML parsing library
- **SQLite**: Lightweight database for caching scraped content (with potential future expansion to PostgreSQL)
- **asyncio**: Python's asynchronous I/O framework
- **Pydantic**: Data validation and settings management
- **Uvicorn**: Fast ASGI server for FastAPI
- **aiosqlite**: Asynchronous SQLite support

## Files Structure

- `fastapi_main.py`: Main FastAPI application entry point
- `flask_main.py`: Optional fallback Flask server
- `backend_async.py`: Core scraping and processing functionality

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/novai-backend.git
   cd novai-backend
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Run FastAPI Backend

1. Start the FastAPI server:
   ```
   uvicorn fastapi_main:app --reload --port 5000
   ```

2. The API will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Run Flask Backend (optional)

1. Start the Flask server:
   ```
   python flask_main.py
   ```

2. The API will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

**Note**: Both FastAPI and Flask servers are configured to run on port 5000 to avoid requiring frontend reconfiguration.

## API Endpoints

### `POST /api/`

Fetches novel content based on keyword, starting chapter, and number of chapters.

**Request Body**:
```json
{
  "keyword": "novel title",
  "chapter": 1,
  "number": 1
}
```

**Response**:
```json
{
  "text": "Plain text content of the novel",
  "title": "Novel Title",
  "image": "URL to novel cover image",
  "formatted": "<p id='par0'>Paragraph 1</p><p id='par1'>Paragraph 2</p>...",
  "array": ["Paragraph 1", "Paragraph 2", ...]
}
```

## How It Works

1. The backend receives a request with novel keyword, starting chapter, and chapter count
2. It searches for the novel on novelfull.com
3. If found, it scrapes the specified chapters
4. Content is processed, formatted, and returned to the frontend
5. Previously scraped content is cached in SQLite for better performance

## Database Schema

The SQLite database (`novels.db`) contains a single table:

```sql
CREATE TABLE IF NOT EXISTS chapters (
    url VARCHAR PRIMARY KEY NOT NULL,
    text TEXT NOT NULL
)
```

## Text Processing

The backend applies several text processing steps:
- Paragraph extraction and cleanup
- Removal of translator notes and copyright information
- Special character handling (e.g., replacing "+" with "plus")
- Preprocessing for smoother text-to-speech output (e.g., removal of visual censorship symbols)
- Formatting text for TTS compatibility

## Performance Considerations

- **Caching**: Novel content is cached in SQLite to reduce load on source websites
- **Asynchronous Processing**: All HTTP requests and processing use asyncio for better performance
- **Pagination Handling**: The code efficiently navigates through paginated content

## CORS Handling

- CORS is configured in both FastAPI and Flask servers, allowing the frontend and backend to communicate during development without cross-origin issues.

## Security Considerations

- The API includes CORS middleware to control access
- Input validation is performed using Pydantic models
- HTML content is carefully sanitized

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[MIT License](LICENSE)

