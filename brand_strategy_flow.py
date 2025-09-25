from llm_central import ask_llm

def process_brand_strategy(session_data, agent, context):
    brand_strategy_fields = [
        "target_audience",
        "competition_analysis",
        "mission_vision_values",
        "brand_identity",
        "brand_archetypes",
        "brand_story",
        "alignment_strategy",
        "metrics_plan"
    ]
    responses = {}
    for field in brand_strategy_fields:
        question = f"ช่วยให้รายละเอียดเกี่ยวกับหัวข้อ '{field}' ของกลยุทธ์แบรนด์ธุรกิจคุณ"
        response = ask_llm(question, agent=agent, context=context)
        responses[field] = response

        # map คำตอบลงใน session_data
        session_data["state"]["brand_strategy"][field] = response

        # เก็บลง history
        session_data["state"]["conversation_history"].append({"role": "user", "content": question})
        session_data["state"]["conversation_history"].append({"role": "assistant", "content": response})

    return responses