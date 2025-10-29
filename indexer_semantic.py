"""Модуль семантического индексирования документов через эмбеддинги"""

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

DOCS_FOLDER = "docs"             # папка с исходными текстами
INDEX_FOLDER = "semantic_index"  # куда сохраняем индекс
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # модель для эмбеддингов
EMBED_DIM = 384                  # размерность вектора модели
TOPK_EXAMPLE = 5                 # сколько ближайших документов выводить для теста

os.makedirs(INDEX_FOLDER, exist_ok=True)

print("Загрузка модели эмбеддингов...")
model = SentenceTransformer(MODEL_NAME)

def load_documents(folder: str):
    texts = []
    filenames = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                text = f.read()
                texts.append(text)
                filenames.append(file)
    print(f"Загружено {len(texts)} документов из {folder}")
    return texts, filenames

def embed_documents(texts):
    print("Генерация эмбеддингов документов...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)  # нормализация для cosine similarity
    return embeddings

def build_faiss_index(embeddings, ids):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)     # inner product на нормализованных векторах = cosine similarity
    index = faiss.IndexIDMap(index)    # хранение соответствия внешних id
    index.add_with_ids(embeddings, np.array(ids, dtype=np.int64))
    return index

def save_index(index, embeddings, filenames, folder=INDEX_FOLDER):
    # Сохраняем FAISS индекс
    faiss_path = os.path.join(folder, "faiss.index")
    faiss.write_index(index, faiss_path)

    # Сохраняем имена файлов
    with open(os.path.join(folder, "filenames.pkl"), "wb") as f:
        pickle.dump(filenames, f)

    # Сохраняем эмбеддинги
    np.save(os.path.join(folder, "embeddings.npy"), embeddings)

    print(f"Индекс, эмбеддинги и имена файлов сохранены в папке {folder}")

def exec_semantic_indexing():
    docs, filenames = load_documents(DOCS_FOLDER)
    embeddings = embed_documents(docs)
    ids = list(range(1, len(docs)+1))
    index = build_faiss_index(embeddings, ids)
    save_index(index, embeddings, filenames)
    
    # Пример поиска (для теста, потом удалим)
    print("\nПример поиска: топ-5 ближайших документов для первого документа...")
    D, I = index.search(embeddings[0:1], TOPK_EXAMPLE)
    for rank, (doc_id, score) in enumerate(zip(I[0], D[0]), start=1):
        print(f"{rank}. ID: {doc_id}, score: {score:.4f}, file: {filenames[doc_id-1]}")

if __name__ == "__main__":
    exec_semantic_indexing()