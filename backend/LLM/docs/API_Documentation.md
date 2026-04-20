# API Documentation

## Endpoint: `POST /process`

### Request Body (JSON)

```json
{
    "chain": [
        {
            "prompt": "string",
            "action": "generate | check | correct | consult",
            "model": "auto (or specific model name)"
        }
    ],
    "user-id": "optional string",
    "mode": "fast | deep | research"
}
```

### Response (200 OK)

```json
{
    "result": "string (final output)",
    "history": [
        {
            "prompt": "...",
            "action": "...",
            "text": "..."
        }
    ]
}
```

### Error Response (400)

```json
{
    "detail": "error description"
}
```
