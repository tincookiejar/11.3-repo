# 라우터 함수: 어떤 에이전트를 실행할지 결정
def route_agent(state: AgentState) -> str:
    # 1. 마지막 메시지 확인
    last_message = state["messages"][-1]
    
    # 2. 도구 호출이 요청된 경우: 도구 실행 후 해당 에이전트를 다시 실행
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print("--- 라우팅 결정: Tool Call - 현재 에이전트 재실행 ---")
        return "continue" # 현재 에이전트를 다시 실행하여 도구 결과를 처리하도록 함
        
    # 3. 마지막 메시지가 ToolMessage인 경우: 도구 결과 처리 후 해당 에이전트를 다시 실행
    if last_message.type == "tool":
        print("--- 라우팅 결정: Tool Message - 현재 에이전트 재실행 ---")
        return "continue" 
        
    # 4. LLM이 'next_agent' 상태를 설정했는지 확인 (컨트롤러/LLM 결정)
    if state.get("next_agent"):
        next_agent_name = state["next_agent"]
        print(f"--- 라우팅 결정: 상태에 정의된 다음 에이전트 ({next_agent_name}) ---")
        # 상태에서 'next_agent' 키를 삭제하고 다음 에이전트 이름 반환
        state["next_agent"] = None
        return next_agent_name
    
    # 5. 최종 답변인지 확인 (예: 'FinalReviewer'의 결정)
    # 실제로는 LLM 응답의 내용을 분석하여 'END'를 결정하는 노드를 추가하는 것이 좋습니다.
    # 여기서는 간단히 마지막으로 실행된 에이전트의 이름으로 가정합니다.
    last_agent = state.get("last_agent") # (이 예제에서는 'last_agent'를 상태에 명시적으로 추가하지 않았지만, 필요할 수 있음)
    if "final answer" in last_message.content.lower() or "답변을 작성" in last_message.content:
         print("--- 라우팅 결정: 최종 답변으로 간주되어 END ---")
         return END
        
    # 6. 기본적으로는 다른 에이전트로 전환
    print("--- 라우팅 결정: Researcher로 전환 (기본값) ---")
    return "Researcher"