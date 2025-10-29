import os
import re
from pymorphy3 import MorphAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unicodedata

INPUT_DIR = "docs"
OUTPUT_DIR = "processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

nltk.download('punkt')
nltk.download('stopwords')

morph = MorphAnalyzer()
stop_words = set(stopwords.words("russian"))

# ---- Очистка текста ----
def clean_text(text: str) -> str:
    # убираем строку URL, если она есть
    text = re.sub(r"^URL:.*\n?", "", text, flags=re.MULTILINE)
    # разложить все символы (в том числе ударные)
    text = unicodedata.normalize("NFD", text)
    # удалить все ударения, тильды и прочие диакритики
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    # убираем цифры и знаки пунктуации
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    # убираем латиницу
    text = re.sub(r"[a-zA-Z]+", " ", text)
    # нижний регистр
    text = text.lower()
    # удаляем лишние пробелы
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---- Основная обработка ----
def preprocess_text(text: str) -> str:
    text = clean_text(text)
    tokens = word_tokenize(text, language="russian")
    # убираем стоп-слова и слишком короткие токены
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    # лемматизация
    lemmas = [morph.parse(t)[0].normal_form for t in tokens]
    return " ".join(lemmas)

def process_all_txt():
    for file_name in os.listdir(INPUT_DIR):
        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(INPUT_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        processed_text = preprocess_text(text)

        out_path = os.path.join(OUTPUT_DIR, file_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(processed_text)

        print(f"✔ Обработан файл: {file_name}")

if __name__ == "__main__":
    process_all_txt()