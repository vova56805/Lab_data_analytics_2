import csv
import json
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv


if len(sys.argv) < 2:
    print("Ошибка: Не указан файл для обработки")
    print("Использование: python3 main.py <файл.csv>")
    sys.exit(1)

input_file = sys.argv[1]


if not os.path.exists(input_file):
    print(f"Ошибка: Файл '{input_file}' не существует")
    sys.exit(1)

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("Ошибка: не найден OPENROUTER_API_KEY. Проверь файл .env")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b:free"

results = []

with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="/")

    if "id" not in reader.fieldnames or "title" not in reader.fieldnames or "text" not in reader.fieldnames:
        print("Ошибка: CSV файл должен содержать колонки 'id', 'title' и 'text'")
        sys.exit(1)

    for row in reader:
        title = row["title"]
        text = row["text"]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Сделай краткое содержание новости.

                    Верни ответ строго в JSON формате:

                    {{
                    "summary": "..."
                    }}

                    Где:
                    summary — краткое содержание новости в 1-2 предложениях

                    Заголовок новости:
                    {title}

                    Текст новости:
                    {text}
                    """,
                }
            ],
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(content)

            results.append(
                {
                    "id": row["id"],
                    "title": title,
                    "summary": parsed["summary"],
                }
            )

            print(f"Обработана новость: {title}")

        except Exception as e:
            print(f"Ошибка при обработке новости: {title}")
            print(content)

output_file = os.path.splitext(input_file)[0] + "_results.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

print(f"Данные сохранены в {output_file}")