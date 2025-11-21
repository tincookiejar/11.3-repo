# 1. StateGraph 초기화
workflow = StateGraph(AgentState)

# 2. 노드 추가
workflow.add_node("Researcher", research_agent)
workflow.add_node("FinalReviewer", reviewer_agent)

# 3. 시작 지점 정의 (항상 Researcher에서 시작)
workflow.set_entry_point("Researcher")

# 4. 조건부 경로 및 일반 경로 추가

# Researcher 노드: Researcher 실행 후, 라우터를 통해 다음 노드 결정
workflow.add_conditional_edges(
    "Researcher",
    # 라우터 함수 호출
    route_agent,
    {
        "Researcher": "Researcher",       # Researcher가 다시 실행되어야 하는 경우 (도구 사용 후)
        "FinalReviewer": "FinalReviewer", # FinalReviewer로 통제권 이양
        END: END                        # 워크플로우 종료
    }
)

# FinalReviewer 노드: FinalReviewer 실행 후, 라우터를 통해 다음 노드 결정
workflow.add_conditional_edges(
    "FinalReviewer",
    route_agent,
    {
        "Researcher": "Researcher",       # Researcher로 통제권 반환 (추가 정보 필요 시)
        "FinalReviewer": "FinalReviewer", # FinalReviewer가 다시 실행되어야 하는 경우 (도구 사용 후)
        END: END                        # 워크플로우 종료
    }
)

# 5. 그래프 컴파일
app = workflow.compile()

# (선택 사항: 그래프 시각화)
# app.get_graph().draw(output_file="a2a_graph.png")