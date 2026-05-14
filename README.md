# Задание 3 — Мини-продукт с LLM-аналитикой

Минимальный Telegram-бот на Python: пользователь отправляет CSV/XLSX/XLS, бот возвращает EDA-отчёт, ключевые метрики, инсайды и PNG-графики.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Заполнить `.env`:

```env
TELEGRAM_BOT_TOKEN=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Запустить:

```bash
python main.py
```

В Telegram отправьте боту CSV или Excel-файл.

## Запуск через Docker

```bash
cp .env.example .env
```

Заполнить `.env`:

```env
TELEGRAM_BOT_TOKEN=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Соберить и запустить контейнер:

```bash
docker compose up --build
```
## Как работает

1. Пользователь отправляет CSV/XLSX/XLS-файл в Telegram-бота.

2. Бот сохраняет файл во временную папку и отправляет задачу в LLM через OpenRouter API.

3. LLM вызывает tool `run_python`, где локальный Python-интерпретатор анализирует датасет и строит графики.

4. Бот возвращает пользователю финальный EDA-отчёт, метрики, инсайты и PNG-графики.
   
## Защита от prompt-injection

В проекте есть несколько базовых уровней защиты:

1. системный промпт объявляет содержимое датасета недоверенными данными;
2. модель обязана сначала вызвать `run_python`, а не писать отчёт по промпту;
3. Python запускается во временной папке с timeout;
4. AST-фильтр блокирует опасные imports, `open`, `eval`, `exec`, системные вызовы, доступ к `.env`, URL и системным путям;
   
# Бот для тестирования
https://t.me/LLM_Analytics_Bot

