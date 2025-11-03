from typing import Callable, Dict, Any


class ToolRegistry:
def __init__(self):
self.tools: Dict[str, Callable[[Dict[str, Any]], Any]] = {}


def register(self, name: str, func: Callable[[Dict[str, Any]], Any]):
self.tools[name] = func


def call(self, name: str, payload: Dict[str, Any]):
if name not in self.tools:
raise ValueError(f"Tool not found: {name}")
return self.tools[name](payload)


# 예: 간단한 웹검색/파일검색 도구 자리표시자
registry = ToolRegistry()




def web_search_tool(payload):
# 실제 구현에서는 로컬 크롤러/검색 API 연결
query = payload.get("query", "")
return {"results": [f"(stub) search result for: {query}"]}




def file_search_tool(payload):
# 실제 구현에서는 문서 DB/인덱스 연결
query = payload.get("query", "")
return {"results": [f"(stub) file result for: {query}"]}


registry.register("web.search", web_search_tool)
registry.register("file.search", file_search_tool)