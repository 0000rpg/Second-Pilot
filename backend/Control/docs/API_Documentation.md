# API Documentation

Base URL: `http://localhost:<PORT>`

---

## Health Check

### `GET /health`

**Response (200 OK)**

```json
{ "ok": true }
```

---

## Auth

### `POST /auth/register`

Регистрация нового пользователя. Возвращает JWT-токен.

**Request Body (JSON)**

```json
{
    "login": "string",
    "password": "string"
}
```

**Response (201 Created)**

```json
{
    "ok": true,
    "token": "string (JWT)",
    "username": "string"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"login and password are required"` / `"invalid request body"` |
| 409  | `"username already taken"` |
| 500  | `"internal server error"` |

---

### `POST /auth/login`

Авторизация существующего пользователя. Возвращает JWT-токен.

**Request Body (JSON)**

```json
{
    "login": "string",
    "password": "string"
}
```

**Response (200 OK)**

```json
{
    "ok": true,
    "token": "string (JWT)",
    "username": "string"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"login and password are required"` / `"invalid request body"` |
| 401  | `"invalid username or password"` |
| 500  | `"internal server error"` |

---

### `GET /auth/verify`

Проверка валидности JWT-токена.

**Headers**

```
Authorization: Bearer <token>
```

**Response (200 OK)**

```json
{
    "ok": true,
    "token": "string (JWT)",
    "username": "string"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 401  | `"missing or invalid authorization header"` / `"invalid or expired token"` |

---

## Chats

> Все эндпоинты требуют заголовок `Authorization: Bearer <token>`.

### `GET /chats`

Получить все чаты текущего пользователя.

**Response (200 OK)**

```json
{
    "ok": true,
    "chats": [
        {
            "id": 1,
            "user_id": 42,
            "name": "string",
            "messages": [],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

---

### `POST /chats`

Создать новый чат.

**Request Body (JSON)**

```json
{
    "name": "string (optional, default: \"Новый чат\")"
}
```

**Response (201 Created)**

```json
{
    "ok": true,
    "chat": {
        "id": 1,
        "user_id": 42,
        "name": "string",
        "messages": [],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
}
```

---

### `GET /chats/{id}`

Получить чат по ID.

**Response (200 OK)**

```json
{
    "ok": true,
    "chat": {
        "id": 1,
        "user_id": 42,
        "name": "string",
        "messages": [],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"invalid chat id"` |
| 404  | `"chat not found"` |
| 500  | `"internal server error"` |

---

### `PUT /chats/{id}`

Обновить имя и/или сообщения чата.

**Request Body (JSON)**

```json
{
    "name": "string",
    "messages": []
}
```

**Response (200 OK)**

```json
{ "ok": true }
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"invalid chat id"` / `"invalid request body"` / `"name is required"` |
| 500  | `"internal server error"` |

---

### `DELETE /chats/{id}`

Удалить чат по ID.

**Response (200 OK)**

```json
{ "ok": true }
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"invalid chat id"` |
| 500  | `"internal server error"` |

---

## Admin

> Все эндпоинты требуют заголовок `Authorization: Bearer <token>`.

### `GET /admin/users`

Получить список всех пользователей.

**Response (200 OK)**

```json
{
    "ok": true,
    "users": [
        {
            "id": 1,
            "username": "string"
        }
    ]
}
```

---

### `POST /admin/users`

Создать нового пользователя.

**Request Body (JSON)**

```json
{
    "login": "string",
    "password": "string"
}
```

**Response (201 Created)**

```json
{
    "ok": true,
    "user": {
        "id": 1,
        "username": "string"
    }
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"login and password are required"` / `"invalid request body"` |
| 409  | `"username already taken"` |
| 500  | `"internal server error"` |

---

### `PUT /admin/users/{id}`

Переименовать пользователя.

**Request Body (JSON)**

```json
{
    "login": "string"
}
```

**Response (200 OK)**

```json
{ "ok": true }
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"invalid user id"` / `"invalid request body"` / `"login is required"` |
| 409  | `"username already taken"` |
| 500  | `"internal server error"` |

---

### `DELETE /admin/users/{id}`

Удалить пользователя по ID.

**Response (200 OK)**

```json
{ "ok": true }
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400  | `"invalid user id"` |
| 500  | `"internal server error"` |

---

## Auth Details

JWT-токены выпускаются с помощью алгоритма **HS256**. Срок действия — **24 часа**.

Секрет задаётся переменной окружения `JWT_SECRET`.

Полезная нагрузка токена (claims):

```json
{
    "user_id": 1,
    "username": "string",
    "exp": 1234567890,
    "iat": 1234567890
}
```

---

## Error Response Format

Все ошибки возвращаются в едином формате:

```json
{
    "ok": false,
    "error": "error description"
}
```
