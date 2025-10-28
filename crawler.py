"""Модуль, отвечающий за загрузку текстов из Интернета"""

import wikipediaapi
import os

wiki = wikipediaapi.Wikipedia(
    language='ru',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='crawler',
    timeout=30
)

SAVE_FOLDER = "docs"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def save_document(text, url, doc_id, folder=SAVE_FOLDER):
    """Сохраняет текст статьи и URL в файл"""
    file_path = os.path.join(folder, f"{doc_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n\n{text}")
    return file_path

def fetch_wikipedia_page(title):
    """Получает текст и URL статьи"""
    page = wiki.page(title)
    if page.exists():
        return page.text, page.fullurl, page.links  # текст, ссылка, связанные статьи
    else:
        return None, None, None

def crawl_category(category_name, max_articles=50, start_id=0):
    category_page = wiki.page("Категория:" + category_name)
    if not category_page.exists():
        print(f"Категория {category_name} не найдена")
        return start_id

    queue = list(category_page.categorymembers.values())
    visited = set()
    doc_id = start_id

    while queue and doc_id - start_id < max_articles:
        page = queue.pop(0)
        if page.title in visited:
            continue
        visited.add(page.title)

        if page.ns == wikipediaapi.Namespace.MAIN and page.exists():
            text = page.text
            url = page.fullurl
            save_document(text, url, doc_id)
            print(f"Сохранена статья: {page.title} ({url})")
            doc_id += 1

        try:
            for member in page.categorymembers.values():
                if member.title not in visited:
                    queue.append(member)
        except KeyError:
            continue

    return doc_id

if __name__ == "__main__":
    import os
    os.makedirs("docs", exist_ok=True)

    start_categories = ["Животные", "Млекопитающие", "Космос"]

    doc_id = 0
    for category in start_categories:
        doc_id = crawl_category(category, max_articles=5, start_id=doc_id)