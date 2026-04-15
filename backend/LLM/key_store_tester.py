import os
from dotenv import load_dotenv
import secrets

# 1. Генерация криптографически безопасного секретного ключа
secret_key = secrets.token_hex(32)  # 32 байта = 64 hex символа

# 2. Сохранение в .env файл (ТОЛЬКО для разработки!)
if False:
    with open("keys.env", "w") as f:
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write(f"DB_PASSWORD=your_database_password\n")

# 3. Загрузка переменных из .env файла в системное окружение
load_dotenv("keys.env")  # Загружает переменные из .env в os.environ

# 4. Использование в приложении
stored_password = os.getenv("DB_PASSWORD")
print(f"Пароль из переменных окружения: {stored_password}")

# Альтернативный способ с значением по умолчанию
api_key = os.getenv("SECRET_KEY", "default-key-if-not-set")
print(f"Ключ из переменных окружения: {api_key}")
