import os




class SearchAgent:
def __init__(self, cfg: AgentConfig, rag: RAGIndexer):
self.llm = _llm(cfg)
self.rag = rag


def search(self, keywords: list[str]) -> Dict[str, Any]:
query = ", ".join(keywords) if keywords else "일반 검색"
hits = self.rag.query(query, top_k=5)
# 요약은 LLM에게 위임
joined = "\n\n".join([f"[출처:{h['source']}]\n{h['content']}" for h in hits])
prompt = f"<system>\n{SYSTEM_SEARCH}\n</system>\n<user>키워드: {query}\n자료:\n{joined}</user>"
out = self.llm.invoke(prompt)
try:
import json
return json.loads(out)
except Exception:
return {"snippets": hits, "summary": out}




class WriterAgent:
def __init__(self, cfg: AgentConfig):
self.llm = _llm(cfg)


def write(self, outline: list[str], search_summary: str) -> str:
outline_txt = "\n- ".join(["" + o for o in outline])
prompt = (
f"<system>\n{SYSTEM_WRITER}\n</system>\n"
f"<user>개요:\n- {outline_txt}\n\n검색 요약:\n{search_summary}</user>"
)
return self.llm.invoke(prompt)




class ReviewerAgent:
def __init__(self, cfg: AgentConfig):
self.llm = _llm(cfg)


def review(self, draft: str, checklist: list[str]) -> Dict[str, Any]:
checklist_txt = "\n- ".join(["" + c for c in checklist])
prompt = (
f"<system>\n{SYSTEM_REVIEWER}\n</system>\n"
f"<user>체크리스트:\n- {checklist_txt}\n\n작성본:\n{draft}</user>"
)
out = self.llm.invoke(prompt)
try:
import json
return json.loads(out)
except Exception:
return {"issues": [], "suggestions": [out], "final_score": 0.8}