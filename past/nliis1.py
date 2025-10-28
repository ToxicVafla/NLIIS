import datetime
import re
from collections import Counter
import math


class Document:
    _next_id = 1  # id autoincrement
    
    def __init__(self, title: str, text: str, datetime: str = ""):
        self.document_id = Document._next_id
        Document._next_id += 1
        self.title = title
        self.text = text
        self.datetime = datetime


class Indexer:
    def __init__(self):
        self.document_base = {}
        self.term_index = {}  # {term: set(document_id)}



    def get_document_vector(self, document_id: int): # 2.1-2.2 2.1 main function, here we create vector from raw document
        doc = self.document_base[document_id]
        words = doc.text.lower().split()
        vector = {}
        for word in set(words):
            vector[word] = self.get_lemm_weight_in_document(word, document_id)
        return vector

    def add_document_to_base(self, filepath: str): # 1. open file, create Document instance
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        
        title = filepath.split("/")[-1]
        
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        doc = Document(title, text, datetime_str)

        self.document_base[doc.document_id] = doc

        return

    def get_lemm_inverse_frequency(self, term): # IDF
        N = len(self.document_base)
        Pi = len(self.term_index.get(term, []))
        if Pi == 0:
            return 0
        return math.log(N / Pi)

    def get_lemm_weight_in_document(self, term, document_id): # TF-IDF
        doc = self.document_base[document_id]
        tf = doc.text.lower().split().count(term)  # простая частота
        idf = self.get_lemm_inverse_frequency(term)
        return tf * idf

    def del_document_from_base(self): # 3.
        pass

index_machine = Indexer()

index_machine.add_document_to_base("texts/parks.txt")

vec1 = index_machine.get_document_vector(1)  # документ с id=1

index_machine.add_document_to_base("texts/borsch.txt")

vec2 = index_machine.get_document_vector(2)  # документ с id=2

index_machine.add_document_to_base("texts/idf.txt")

vec3 = index_machine.get_document_vector(3)  # документ с id=3



print("Вес 'и' в doc1:", index_machine.get_lemm_weight_in_document("и", 1))
