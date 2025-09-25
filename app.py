import streamlit as st
import uuid
from session_manager import load_session, save_session
from llm_central import ask_llm
import json
from datetime import datetime

st.set_page_config(page_title="AI โค้ชธุรกิจ SME", page_icon="🚀")
st.markdown("<style>body {background: #f7f9fc;}</style>", unsafe_allow_html=True)
st.title("AI โค้ชธุรกิจสำหรับ SME / ผู้ประกอบการ 🚀")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id
session_data = load_session(session_id)

brand_strategy_fields = [
    {"key": "target_audience", "question": "กลุ่มเป้าหมายเราเป็นใคร?"},
    {"key": "brand_identity", "question": "อัตลักษณ์แบรนด์ของคุณคืออะไร?"},
    {"key": "brand_archetypes", "question": "ต้นแบบแบรนด์ของคุณคืออะไร?"},
    {"key": "competition_analysis", "question": "วิเคราะห์คู่แข่งของธุรกิจคุณ"},
    {"key": "mission_vision_values", "question": "พันธกิจ วิสัยทัศน์ และค่านิยมของแบรนด์"},
    {"key": "brand_story", "question": "เรื่องราวแบรนด์ของคุณ"},
    {"key": "alignment_strategy", "question": "กลยุทธ์การสร้าง Alignment ในองค์กร"},
    {"key": "metrics_plan", "question": "แผนการวัดผลสำเร็จของแบรนด์"},
    {"key": "vendor_recommendations", "question": "มีผู้ให้บริการหรือ vendor ด้านนี้ที่แนะนำไหม?"},
]

if not session_data:
    session_data = {
        "session_id": session_id,
        "state": {
            "brand_strategy": {field["key"]: None for field in brand_strategy_fields},
            "conversation_history": [],
        }
    }

# state สำหรับ flow ของการถามทีละข้อ
if "bs_step" not in st.session_state:
    st.session_state.bs_step = 0
if "bs_answers" not in st.session_state:
    st.session_state.bs_answers = {}
if "bs_bot_reply" not in st.session_state:
    st.session_state.bs_bot_reply = {}

# --- Custom CSS for chat bubbles ---
st.markdown("""
<style>
.bubble-user {
  background: #464646;
  border-radius: 18px 18px 18px 4px;
  padding: 12px 18px;
  margin-bottom: 6px;
  box-shadow: 0 1px 4px rgba(0,0,0,.12);
  display: inline-block;
  max-width: 70%;
}
.bubble-bot {
  background: #464646;
  border-radius: 18px 18px 4px 18px;
  padding: 12px 18px;
  margin-bottom: 18px;
  box-shadow: 0 1px 4px rgba(0,0,0,.12);
  display: inline-block;
  max-width: 70%;
}
.bubble-row {
  display: flex; flex-direction: row; align-items: flex-end; margin-bottom: 2px;
}
.bubble-row.user { justify-content: flex-start; }
.bubble-row.bot { justify-content: flex-end; }
.avatar { width: 36px; height: 36px; border-radius: 50%; margin-right: 10px; }
.avatar-bot { margin-left: 10px; }
.timestamp { font-size: 12px; color: #b0b0b0; margin-left: 12px; }
</style>
""", unsafe_allow_html=True)

st.subheader("Brand Strategy Chat")

# --- Render chat history (bubbles) ---
for i in range(st.session_state.bs_step):
    field = brand_strategy_fields[i]
    user_ans = st.session_state.bs_answers.get(field["key"], "")
    bot_ans = st.session_state.bs_bot_reply.get(field["key"], "")
    ts = datetime.now().strftime("%H:%M")
    # User bubble (left)
    st.markdown(
        f"""
        <div class='bubble-row user'>
            <img src='https://randomuser.me/api/portraits/men/10.jpg' class='avatar'/>
            <span class='bubble-user'><b>คุณ:</b> {user_ans}</span>
            <span class='timestamp'>{ts}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Bot bubble (right)
    if bot_ans:
        st.markdown(
            f"""
            <div class='bubble-row bot'>
                <span class='timestamp'>{ts}</span>
                <span class='bubble-bot'><b>โค้ช:</b> {bot_ans}</span>
                <img src='https://randomuser.me/api/portraits/lego/2.jpg' class='avatar avatar-bot'/>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- ถามข้อถัดไป ---
if st.session_state.bs_step < len(brand_strategy_fields):
    current_field = brand_strategy_fields[st.session_state.bs_step]
    st.markdown(f"<div class='bubble-row bot'><span class='bubble-bot'><b>โค้ชถาม:</b> {current_field['question']}</span></div>", unsafe_allow_html=True)
    user_reply = st.text_input("ตอบที่นี่", key=f"bs_answer_{st.session_state.bs_step}")
    if user_reply:
        st.session_state.bs_answers[current_field["key"]] = user_reply
        session_data["state"]["brand_strategy"][current_field["key"]] = user_reply
        session_data["state"]["conversation_history"].append({"role": "user", "content": user_reply})

        # --- ปรับ prompt สำหรับ vendor โดยเฉพาะ ---
        if current_field["key"] == "vendor_recommendations":
            prompt = (
                f"หัวข้อ: {current_field['question']}\n"
                f"คำตอบของผู้ใช้: {user_reply}\n"
                "ช่วยแนะนำรายชื่อ vendor หรือผู้ให้บริการที่เกี่ยวข้องในประเทศไทยหรือสากล พร้อมข้อมูลติดต่อ หรือช่องทางค้นหาเพิ่มเติม"
            )
        else:
            prompt = (
                f"หัวข้อ: {current_field['question']}\n"
                f"คำตอบของผู้ใช้: {user_reply}\n"
                "ช่วยให้ feedback เพิ่มเติม หรือข้อแนะนำในฐานะโค้ชธุรกิจ"
            )

        bot_reply = ask_llm(prompt)
        st.session_state.bs_bot_reply[current_field["key"]] = bot_reply
        session_data["state"]["conversation_history"].append({"role": "assistant", "content": bot_reply})

        save_session(session_data)
        st.session_state.bs_step += 1
        st.rerun()

# --- สรุปครบทุกข้อ ---

if st.session_state.bs_step == len(brand_strategy_fields):
    st.success("คุณตอบครบทุกหัวข้อแล้ว!")
    st.json(session_data["state"]["brand_strategy"])

    if st.button("สร้าง Business Pitch แบบอัตโนมัติ (สั้น/เต็ม พร้อมแนะนำ vendor และตัวอย่างจริง)"):
        # รวมทุกคำตอบเป็น context
        pitch_context = "\n".join(
            [
                f"{field['question']} {st.session_state.bs_answers.get(field['key'], '')}"
                for field in brand_strategy_fields
            ]
        )

        # Prompt สำหรับ LLM
        pitch_prompt = (
            "นี่คือข้อมูลวางแผนธุรกิจที่ผู้ใช้ตอบในแต่ละหัวข้อ:\n"
            f"{pitch_context}\n\n"
            "กรุณาสรุปออกมาเป็น Business Pitch แบบย่อ 1 ย่อหน้า สำหรับใช้ขายไอเดียกับนักลงทุนหรือพาร์ทเนอร์ "
            "และแบบเต็ม (ละเอียด ชูจุดเด่น กลยุทธ์ ฯลฯ) "
            "พร้อมแนะนำ vendor ที่เกี่ยวข้อง (ไทย/สากล) และตัวอย่างเคสธุรกิจจริงที่ประสบความสำเร็จในด้านนี้ด้วย"
        )
        pitch = ask_llm(pitch_prompt)

        # แสดงผลในแชท Bubble
        st.markdown("""
        <div class='bubble-row bot'>
            <span class='bubble-bot'><b>Business Pitch + Vendor & Case Example:</b><br>{}</span>
        </div>
        """.format(pitch), unsafe_allow_html=True)