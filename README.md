# GenAI Information Improvement App

This project provides a simple FastAPI and Streamlit application that uses Google Gemini to improve short pieces of information.

The app accepts text containing 10 to 50 characters, sends it to a FastAPI backend, receives an improved response, and optionally saves the input/output pair in a SQLite database.

## Project structure

```text
GenAI_App_Data_Improvement/
├── src/
│   ├── api/
│   │   └── fastapi_api.py       # Gemini-backed FastAPI service
│   ├── app/
│   │   └── streamlit_app.py     # Streamlit user interface
│   └── dao/
│       └── improvement_dao.py   # SQLite create/save/load operations
├── .env                          # Local API configuration
├── requirements.txt
└── Improvement.db                # Created automatically by the app
```

## Features

- Improve short text through Google Gemini.
- Validate input length and blank values.
- Call the improvement service through a local FastAPI backend.
- Display the original and improved information in Streamlit.
- Save successful improvements in a SQLite database.
- View previously saved improvements.

## Prerequisites

- Python 3.10 or newer
- A Google Gemini API key
- Windows Command Prompt, PowerShell, or a VS Code terminal

## Setup

From the project root, create and activate a virtual environment:

```powershell
uv venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt activation instead:

```bat
.venv\Scripts\activate.bat
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Do not commit `.env` or an API key to source control.

## Run the application

Keep the backend and frontend in two separate terminals.

### Terminal 1: Start FastAPI

```powershell
python -m fastapi dev src/api/fastapi_api.py
```

The backend runs at `http://127.0.0.1:8000`.

Open `http://127.0.0.1:8000/docs` to view the Swagger interface and test the API.

### Terminal 2: Start Streamlit

```powershell
python -m streamlit run src/app/streamlit_app.py
```

Streamlit will open the application in your browser, typically at `http://localhost:8501`.

Other supported launch commands:

```powershell
fastapi dev src/api/fastapi_api.py
uv run fastapi dev src/api/fastapi_api.py
streamlit run src/app/streamlit_app.py
uv run streamlit run src/app/streamlit_app.py
```

## API

### `GET /`

Health and welcome endpoint.

Response:

```json
{
  "message": "Welcome To Data Improvement API"
}
```

### `POST /improve`

Improves one text value.

Request:

```json
{
  "request": "Improving data quality"
}
```

Response:

```json
{
  "response": "Improved text returned by Gemini"
}
```

Input must contain 10 to 50 characters and cannot be blank.

## Database

The SQLite database is created automatically at:

```text
Improvement.db
```

The `improvement` table contains:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `input` | TEXT | Original information |
| `output` | TEXT | Gemini-improved information |

Use the **Save to database** button in Streamlit to save the current result. Saved entries appear in **Saved history**.

## Configuration

The backend requires:

```env
GOOGLE_API_KEY=your_google_api_key
```

The Streamlit app can also override the backend URL:

```env
ANALYSIS_API_URL=http://127.0.0.1:8000/improve
```

The default backend URL is `http://127.0.0.1:8000/improve`.

## Troubleshooting

- If Streamlit reports that it could not process the API response, verify that FastAPI is running on port `8000`.
- If FastAPI returns a `503` response, verify that `GOOGLE_API_KEY` exists in `.env`.
- If FastAPI returns a `502` response, the Gemini request or structured response failed; check the API key and service availability.
- If no result is displayed, enter text that is at least 10 and no more than 50 characters.

