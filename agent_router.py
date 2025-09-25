def route_message(user_input, state):
    # เลือก agent ตาม current_phase หรือ keyword
    phase = state.get("current_phase", "")
    if phase == "business_discovery":
        return "Brand Strategy Expert"
    elif phase == "brand_strategy":
        return "Brand Strategy Expert"
    elif phase == "marketing_strategy":
        return "Marketing Strategy Expert"
    elif phase == "solution":
        return "Solution Implementation Expert"
    # fallback ให้ brand ก่อน
    return "Brand Strategy Expert"