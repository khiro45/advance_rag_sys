# FastAPI Starter

A basic FastAPI project template.

## Setup Instructions

1.  **Create a Virtual Environment** (if not already done):

    ```powershell
    python -m venv venv
    ```

2.  **Activate the Virtual Environment**:
    - Windows:
      ```powershell
      .\venv\Scripts\activate
      ```
    - macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the app with auto-reload:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the app is running, you can access:

- Interactive Docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative Docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
