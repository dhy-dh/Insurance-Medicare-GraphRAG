# Streamlit UI

## Quick Start

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run UI
```bash
streamlit run app.py
```

The UI will open at http://localhost:8501

## Configuration

Set the backend URL:
```bash
export BACKEND_URL=http://localhost:8000
streamlit run app.py
```

Or modify the default in `app.py`:
```python
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
```

## Features

- Question input with example buttons
- Answer display with confidence level
- Citation list with expandable details
- Debug information (linked entities, cypher query)
- System health status in sidebar
- Adjustable parameters (hop count, evidence limit)
