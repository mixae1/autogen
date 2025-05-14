import os
import pickle

from langchain_community.vectorstores import FAISS

def has_db(filename):
    return os.path.exists(filename)

def get_faiss_db(filename, emb):
    if os.path.exists(filename):
        print(f'{filename} exists, reusing...')
        with open(filename, 'rb') as file:
            db = FAISS.deserialize_from_bytes(
                embeddings=emb,
                serialized=pickle.load(file),
                allow_dangerous_deserialization=True
            )
        return db

def save_faiss_db(filename, db):
    with open(filename, 'wb') as file:
        pickle.dump(db.serialize_to_bytes(), file)
    return db

def save_faiss_docs(filename, docs, emb):
    db = FAISS.from_documents(docs, emb)
    save_faiss_db(filename, db)
    return db



def get_db(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

def save_db(filename, db):
    with open(filename, 'wb') as file:
        pickle.dump(db, file)
    return db