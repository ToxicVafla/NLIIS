import datetime

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


    def get_document_vector(self): # 2.1-2.2 2.1 main function, here we create vector from raw document
        pass

    def add_document_to_base(self, filepath: str): # 1. open file, create Document instance
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        
        title = filepath.split("/")[-1]
        
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        doc = Document(title, text, datetime_str)

        self.document_base[doc.document_id] = doc

        return

    def get_lemm_inverse_frequency(self): # 2.2 IDF
        pass

    def get_word_weight_in_document(self): # 2.2
        pass

    def get_lemm_weight_in_document(self): # 2.2
        pass

    def del_document_from_base(self): # 3.
        pass

index_machine = Indexer()

index_machine.add_document_to_base("texts/parks.txt")