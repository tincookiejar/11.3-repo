initial_state = {"messages": [("human", "2025년 AI 트렌드에 대해 조사해 줘.")], "next_agent": None}

print("=== A2A 워크플로우 시작 ===")
# 상태 변화를 스트리밍하여 확인
for s in app.stream(initial_state):
    print("--- 새로운 상태 업데이트 ---")
    print(s)
    
print("\n=== 최종 결과 ===")
final_state = app.invoke(initial_state)
print(final_state["messages"][-1].content)