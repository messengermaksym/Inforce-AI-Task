# AI Chat REST API

Реалізація REST API для чату з підтримкою історії повідомлень та автоматичним розрахунком вартості використання токенів.

## Функціонал

- **Керування сесіями:** створення унікальних чат-сесій для розділення діалогів.
- **Контекстна пам'ять:** повноцінна підтримка історії повідомлень у межах кожної сесії.
- **Трекінг витрат:** автоматичне отримання даних про використані токени та розрахунок вартості кожного повідомлення.
- **Історія та статистика:** отримання повного логу діалогу з накопиченою вартістю всієї сесії.
- **Інтерфейс:** веб-інтерфейс для тестування (темна тема, індикатор завантаження, обробка помилок).

## Технології

- **API:** FastAPI
- **AI:** Google Gemini API (модель Gemini 2.5 Flash), SDK `google-genai`
- **БД:** SQLAlchemy (за замовчуванням SQLite)
- **Конфігурація:** змінні середовища через `.env` та `pydantic-settings`

## Структура проєкту

```
Inforce-AI-Task/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI додаток, підключення маршрутів і статики
│   ├── config.py         # Налаштування з .env (Pydantic Settings)
│   ├── database.py       # Підключення до БД, сесії
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── sessions.py   # Ендпоінти сесій та повідомлень
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py       # SQLAlchemy: ChatSession, Message
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini.py     # Клієнт Gemini, розрахунок вартості
│   └── static/          # UI: index.html, style.css, app.js
├── run.py                # Точка запуску сервера
├── .env.example          # Приклад змінних середовища
├── requirements.txt
├── README.md
└── CONTRIBUTING.md       # Конвенція комітів (Conventional Commits)
```

## Встановлення та запуск

1. **Клонувати проєкт та встановити залежності:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Налаштувати змінні середовища:**

   Скопіюйте `.env.example` у `.env` і вкажіть API-ключ:

   ```bash
   cp .env.example .env
   # Відредагуйте .env: GEMINI_API_KEY=ваш_ключ
   ```

   Опційно в `.env` можна задати:
   - `GEMINI_MODEL_ID` — модель (за замовчуванням `gemini-2.5-flash`)
   - `GEMINI_INPUT_PRICE_PER_MILLION`, `GEMINI_OUTPUT_PRICE_PER_MILLION` — ціни за 1M токенів
   - `DATABASE_URL` — підключення до БД (за замовчуванням `sqlite:///./sql_app.db`)

3. **Запустити сервер:**

   ```bash
   python run.py
   ```
   або:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Тестування:**
   - UI: http://127.0.0.1:8000/
   - Swagger: http://127.0.0.1:8000/docs

## API Endpoints

- `POST /sessions` — створення нової чат-сесії.
- `POST /sessions/{id}/messages?message_text=...` — надсилання повідомлення (повертає відповідь та вартість).
- `GET /sessions/{id}/history` — перегляд історії повідомлень та загальної вартості сесії.

## Історія комітів

Для підтримки читабельної історії використовуйте [Conventional Commits](https://www.conventionalcommits.org/). Деталі — у [CONTRIBUTING.md](CONTRIBUTING.md).
