import json
import os

DATA_DIR = "data"

def load_session(session_id):
    """
    โหลดข้อมูล session จากไฟล์ data/{session_id}.json
    ถ้าไฟล์ไม่มีหรือไฟล์ว่าง จะคืน dict ว่าง
    """
    path = os.path.join(DATA_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        # ถ้าไม่มีไฟล์ session ให้คืน dict ว่าง
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
            if not data.strip():
                # ถ้าไฟล์ว่าง
                return {}
            return json.loads(data)
    except Exception as e:
        print(f"Error loading session {session_id}: {e}")
        return {}

def save_session(session_data):
    """
    เซฟข้อมูล session ลงไฟล์ data/{session_id}.json
    """
    session_id = session_data.get("session_id")
    if not session_id:
        print("session_id not found in session_data")
        return
    path = os.path.join(DATA_DIR, f"{session_id}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving session {session_id}: {e}")