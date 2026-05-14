# Telegram LLM Analytics Bot

Минимальный Telegram-бот на Python: пользователь отправляет CSV/XLSX/XLS, бот возвращает EDA-отчёт, ключевые метрики, инсайты и PNG-графики.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`:

```env
TELEGRAM_BOT_TOKEN=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Запустите:

```bash
python main.py
```

В Telegram отправьте боту CSV или Excel-файл.

## Запуск через Docker

```bash
cp .env.example .env
```

Заполните `.env`:

```env
TELEGRAM_BOT_TOKEN=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Соберите и запустите контейнер:

```bash
docker compose up --build
```

## Защита от prompt-injection

В проекте есть несколько базовых уровней защиты:

1. системный промпт объявляет содержимое датасета недоверенными данными;
2. модель обязана сначала вызвать `run_python`, а не писать отчёт по промпту;
3. Python запускается во временной папке с timeout;
4. AST-фильтр блокирует опасные imports, `open`, `eval`, `exec`, системные вызовы, доступ к `.env`, URL и системным путям;



