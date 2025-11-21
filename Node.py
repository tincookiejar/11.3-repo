from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END

# 예시 도구: 에이전트가 사용할 수 있는 도구
@tool
def search_web(query: str) -> str:
    """웹 검색을 수행하고 결과를 반환합니다."""
    # 실제로는 Google Search API 등을 사용합니다.
    return f"웹 검색 결과: '{query}'에 대한 최신 정보는 2025년 AI 동향에 대한 내용입니다."

# 에이전트 정의 (각 에이전트는 State를 받아 새로운 State를 반환)
class BasicAgent:
    def __init__(self, name: str, system_prompt: str, tools: list):
        self.name = name
        self.llm = ChatOpenAI(model="gpt-4o-mini") # 또는 원하는 모델 사용
        self.tools = tools
        self.system_prompt = system_prompt
        
    def __call__(self, state: AgentState) -> AgentState:
        print(f"\n>>> 에이전트 실행: {self.name}")
        
        # 시스템 프롬프트 설정
        messages = [("system", self.system_prompt)] + state["messages"]
        
        # LLM 호출
        response = self.llm.invoke(messages, tools=self.tools)
        
        # LLM 응답이 도구 호출을 요청했는지 확인 (Tool Calling)
        if response.tool_calls:
            messages = state["messages"] + [response]
            for tc in response.tool_calls:
                tool_output = self.handle_tool_call(tc)
                messages.append(tool_output) # ToolMessage 추가
            # 다음 턴에 다시 LLM 호출을 위해 상태 업데이트
            return {"messages": messages} 
            
        # 일반 응답일 경우 (대화 응답)
        return {"messages": state["messages"] + [response]}
        
    def handle_tool_call(self, tool_call):
        # 도구 실행 로직
        tool_name = tool_call.function.name
        tool_args = dict(tool_call.function.arguments)
        
        # 사용할 수 있는 도구 찾기
        for t in self.tools:
            if t.name == tool_name:
                output = t.invoke(tool_args)
                print(f"--- 도구 호출: {tool_name} | 결과: {output[:30]}...")
                return ("tool", output, {"tool_call_id": tool_call.id})
                
        raise ValueError(f"알 수 없는 도구: {tool_name}")

# 두 에이전트 인스턴스 생성
research_agent = BasicAgent(
    name="Researcher",
    system_prompt="당신은 웹 검색을 통해 정보를 수집하는 전문가입니다. 필요한 경우 'search_web' 도구를 사용하여 정보를 찾고, 결과를 바탕으로 답변하십시오. 결과를 얻은 후에는 'next_agent' 상태를 'FinalReviewer'로 설정하여 통제권을 넘기십시오.",
    tools=[search_web]
)

reviewer_agent = BasicAgent(
    name="FinalReviewer",
    system_prompt="당신은 최종 답변을 검토하고 사용자에게 제출할 답변을 작성하는 전문가입니다. 대화 기록을 검토하고 최종 답변이 사용자 질문에 완전히 답변하는지 확인하십시오. 답변이 충분하면 'END'를 반환하십시오. 추가 정보가 필요하면 'next_agent' 상태를 'Researcher'로 설정하십시오.",
    tools=[] # 도구 없음
)