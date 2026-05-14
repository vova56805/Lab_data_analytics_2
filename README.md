# Telegram LLM Analytics Bot

Минимальный Telegram-бот на Python: пользователь отправляет CSV/XLSX/XLS, бот возвращает EDA-отчёт, метрики, инсайты и PNG-графики.

LLM вызывается программно через OpenRouter API. Анализ выполняется не текстовой подстановкой характеристик датасета, а через tool-call `run_python`, который запускает локальный Python-интерпретатор во временной папке.

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
python bot.py
```

В Telegram отправьте боту CSV или Excel-файл.

## Защита от prompt-injection

В проекте есть несколько базовых уровней защиты:

1. системный промпт явно объявляет содержимое датасета недоверенными данными;
2. модель обязана сначала вызвать `run_python`, а не писать отчёт по промпту;
3. Python запускается во временной папке, с очищенным environment и timeout;
4. AST-фильтр блокирует опасные imports, `open/eval/exec`, системные вызовы, доступ к `.env`, URL и системным путям;
5. модель видит только имя файла `DATA_FILE`, а не секреты окружения.

Для продакшена лучше вынести интерпретатор в Docker/MCP-сервер с отключённой сетью, read-only filesystem и лимитами CPU/RAM.
