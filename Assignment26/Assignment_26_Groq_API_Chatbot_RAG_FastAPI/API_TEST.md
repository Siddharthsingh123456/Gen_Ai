# API Test

Start the server:

```bash
uvicorn app:app --reload
```

PowerShell/curl:

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What is RAG?\"}"
```

Swagger is easier on Windows:
`http://127.0.0.1:8000/docs`
