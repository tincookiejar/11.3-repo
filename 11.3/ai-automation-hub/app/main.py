import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv


from .rag import RAGIndexer
from .agents import AgentConfig
from .pipelines import AutomationPipeline


load_dotenv()


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", ".chroma")


app = FastAPI(title="AI Automation Hub")


rag = RAGIndexer(embed_model=EMBED_MODEL, persist_dir=VECTOR_DB_DIR)
agent_cfg = AgentConfig(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
pipeline = AutomationPipeline(cfg=agent_cfg, rag=rag)




class RunRequest(BaseModel):
query: str




@app.get("/")
async def root():
return {"message": "AI Automation Hub is running"}




@app.post("/run")
async def run(req: RunRequest):
result = pipeline.run(req.query)
return result