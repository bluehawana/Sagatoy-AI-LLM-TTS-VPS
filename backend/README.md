# Sagatoyai Backend

AI-powered plush toy backend services.

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Start development server
uvicorn totoyai.main:app --reload
```

## Project Structure

```
backend/
├── src/totoyai/
│   ├── api/          # REST API endpoints
│   ├── models/       # Pydantic data models
│   ├── services/     # STT, LLM, TTS, Weather services
│   └── main.py       # FastAPI application
└── tests/            # Test suite
```
