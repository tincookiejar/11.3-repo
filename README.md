# 11.3-repo

```
ai-automation-hub/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ data/
│ └─ docs/ # RAG용 문서 폴더 (PDF/TXT/MD 등)
├─ app/
│ ├─ main.py # FastAPI 엔트리포인트
│ ├─ agents.py # Controller/Search/Writer/Reviewer agents
│ ├─ rag.py # 임베딩, 벡터DB, 검색기
│ ├─ mcp.py # MCP 유사 도구 레지스트리 및 실행기
│ ├─ prompts.py # 프롬프트 템플릿
│ └─ pipelines.py # 오케스트레이션 파이프라인 (A2A)
└─ scripts/
  └─ ingest.py # 문서 인덱싱 스크립트
a2a rag mcp 다 넣어보고 싶어서 만든겁니다..
```
