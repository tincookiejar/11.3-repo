from typing import Dict, Any
from .agents import ControllerAgent, SearchAgent, WriterAgent, ReviewerAgent, AgentConfig
from .rag import RAGIndexer




class AutomationPipeline:
def __init__(self, cfg: AgentConfig, rag: RAGIndexer):
self.controller = ControllerAgent(cfg)
self.searcher = SearchAgent(cfg, rag)
self.writer = WriterAgent(cfg)
self.reviewer = ReviewerAgent(cfg)


def run(self, user_request: str) -> Dict[str, Any]:
plan = self.controller.plan(user_request)
keywords = plan.get("keywords", [])
outline = plan.get("outline", [])
checklist = plan.get("review_checklist", ["사실성", "명확성", "구조"])


search_res = self.searcher.search(keywords)
summary = search_res.get("summary", "")


draft = self.writer.write(outline, summary)


review = self.reviewer.review(draft, checklist)


return {
"plan": plan,
"search": search_res,
"draft": draft,
"review": review,
}