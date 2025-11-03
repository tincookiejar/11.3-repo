import os
from typing import List, Dict


import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer




class RAGIndexer:
def __init__(self, embed_model: str, persist_dir: str):
self.embed = SentenceTransformer(embed_model)
self.client = chromadb.Client(Settings(persist_directory=persist_dir, is_persistent=True))
self.collection = self.client.get_or_create_collection("docs")


def _embed(self, texts: List[str]):
return self.embed.encode(texts).tolist()


def add(self, docs: List[Dict]):
# docs: [{"id": str, "content": str, "source": str}]
embeddings = self._embed([d["content"] for d in docs])
self.collection.add(
ids=[d["id"] for d in docs],
embeddings=embeddings,
documents=[d["content"] for d in docs],
metadatas=[{"source": d["source"]} for d in docs],
)


def query(self, text: str, top_k: int = 5):
q = self._embed([text])[0]
res = self.collection.query(query_embeddings=[q], n_results=top_k)
out = []
for doc, meta in zip(res.get("documents", [[]])[0], res.get("metadatas", [[]])[0]):
out.append({"content": doc, "source": meta.get("source", "unknown")})
return out