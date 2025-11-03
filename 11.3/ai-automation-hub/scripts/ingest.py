import os
import uuid
from pathlib import Path


from dotenv import load_dotenv
from app.rag import RAGIndexer


load_dotenv()


EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", ".chroma")


DOCS_DIR = Path("data/docs")
SUPPORT_EXT = {".txt", ".md"}




def read_docs():
docs = []
for p in DOCS_DIR.rglob("*"):
if p.suffix.lower() in SUPPORT_EXT:
content = p.read_text(encoding="utf-8", errors="ignore")
docs.append({
"id": str(uuid.uuid4()),
"content": content,
"source": p.name,
})
return docs




def main():
rag = RAGIndexer(embed_model=EMBED_MODEL, persist_dir=VECTOR_DB_DIR)
docs = read_docs()
if not docs:
print("No docs found in data/docs. Put some .txt or .md files.")
return
rag.add(docs)
print(f"Indexed {len(docs)} docs.")




if __name__ == "__main__":
main()