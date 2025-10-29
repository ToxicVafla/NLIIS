"""Модуль, отвечающий за индексирование текстов с помощью TF-IDF формулы"""

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def load_documents(folder_path: str):
    """
    Загружает все .txt файлы из папки. Каждый файл — один документ.
    """
    documents = []
    filenames = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(text)
                filenames.append(file)
    return documents, filenames


def build_index(documents, max_features=5000):
    """
    Создаёт TF-IDF индекс для всех документов.
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 1),
        min_df=1,  # каждый термин встречающийся хотя бы один раз
    )
    matrix = vectorizer.fit_transform(documents)
    return vectorizer, matrix


def save_index(vectorizer, matrix, filenames, path="index"):
    """
    Сохраняет векторизатор, матрицу и соответствие файлов.
    """
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    with open(os.path.join(path, "tfidf_matrix.pkl"), "wb") as f:
        pickle.dump(matrix, f)
    with open(os.path.join(path, "filenames.pkl"), "wb") as f:
        pickle.dump(filenames, f)

def exec_index():
    folder = "processed"
    docs, files = load_documents(folder)
    vectorizer, matrix = build_index(docs)
    
    print(f"Индекс построен: {matrix.shape[0]} документов, {matrix.shape[1]} признаков.\n")
    
    print("Документы:")
    for i, f in enumerate(files[:5]):  # первые 5 файлов
        print(f"{i}: {f}")
    
    print("\nПризнаки (первые 20 терминов):")
    print(vectorizer.get_feature_names_out()[:20])
    
    first_doc_vector = matrix[0].toarray().flatten()
    top_terms_idx = first_doc_vector.argsort()[-10:][::-1]  # топ 10 терминов
    print(f"\nТоп 10 терминов в документе {files[0]}:")
    for idx in top_terms_idx:
        term = vectorizer.get_feature_names_out()[idx]
        weight = first_doc_vector[idx]
        print(f"{term}: {weight:.3f}")
    
    save_index(vectorizer, matrix, files)

if __name__ == "__main__":
    exec_index()