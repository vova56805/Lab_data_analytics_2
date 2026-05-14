# Telegram LLM Analytics Bot

Минимальный Telegram-бот на Python: пользователь отправляет CSV/XLSX/XLS, бот возвращает EDA-отчёт, ключевые метрики, инсайты и PNG-графики.

LLM вызывается программно через OpenRouter API. Анализ выполняется не текстовой подстановкой характеристик датасета, а через tool-call `run_python`, который запускает локальный Python-интерпретатор во временной папке.

## Переменные окружения

Перед запуском создайте `.env` из шаблона:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
copy .env.example .env
```

Заполните `.env`:

```env
TELEGRAM_BOT_TOKEN=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openai/gpt-4o-mini
```



## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

В Telegram отправьте боту CSV или Excel-файл.

## Запуск через Docker

Перед запуском должен быть установлен и запущен Docker.

Создайте и заполните `.env`:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
copy .env.example .env
```

Соберите и запустите контейнер:

```bash
docker compose up --build
```

Запуск в фоне:

```bash
docker compose up -d --build
```

Просмотр логов:

```bash
docker compose logs -f
```

Остановка:

```bash
docker compose down
```

## Защита от prompt-injection

В проекте есть несколько базовых уровней защиты:

1. системный промпт объявляет содержимое датасета недоверенными данными;
2. модель обязана сначала вызвать `run_python`, а не писать отчёт по промпту;
3. Python запускается во временной папке с timeout;
4. AST-фильтр блокирует опасные imports, `open`, `eval`, `exec`, системные вызовы, доступ к `.env`, URL и системным путям;
5. модель видит только имя файла `DATA_FILE`, а не секреты окружения.

Для продакшена лучше вынести интерпретатор в отдельный Docker/MCP-сервер с отключённой сетью, read-only filesystem и лимитами CPU/RAM.
