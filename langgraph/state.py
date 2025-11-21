from typing import TypedDict, Annotated, List
from langgraph.graph.message import AnyMessage, add_messages

# 워크플로우의 상태를 정의합니다.
class AgentState(TypedDict):
    """
    에이전트가 공유하는 상태를 나타냅니다.

    messages: 대화 기록 (필수)
    next_agent: 다음에 실행할 에이전트의 이름
    """
    messages: Annotated[List[AnyMessage], add_messages]
    next_agent: str