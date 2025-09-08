

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


    @staticmethod
    def get_document_vector(): # 2.1-2.2 2.1 main function, here we create vector from raw document
        pass

    @staticmethod
    def add_document_to_base(): # 1. open file, create Document instance
        pass

    @staticmethod
    def get_lemm_inverse_frequency(): # 2.2 IDF
        pass

    @staticmethod
    def get_word_weight_in_document(): # 2.2
        pass

    @staticmethod
    def get_lemm_weight_in_document(): # 2.2
        pass

    @staticmethod
    def del_document_from_base(): # 3.
        pass