import json
import os

DATA_DIR = "data"

def retrieve_documents(user_input):
    vendors_path = os.path.join(DATA_DIR, "vendors.json")
    cases_path = os.path.join(DATA_DIR, "cases.json")
    results = []

    # ค้น vendor ที่เกี่ยวข้อง
    if os.path.exists(vendors_path):
        try:
            with open(vendors_path, "r", encoding="utf-8") as f:
                vendors = json.load(f)
                for v in vendors:
                    if any(word.lower() in user_input.lower() for word in [v["service"], v["name"]]+v["industry_focus"]):
                        results.append(f"Vendor: {v['name']} — Service: {v['service']} — Website: {v['website']}")
        except Exception as e:
            results.append(f"เกิดข้อผิดพลาดในการอ่าน vendors.json: {e}")

    # ค้น case study ที่เกี่ยวข้อง
    if os.path.exists(cases_path):
        try:
            with open(cases_path, "r", encoding="utf-8") as f:
                cases = json.load(f)
                for c in cases:
                    if c["industry"].lower() in user_input.lower() or c["title"].lower() in user_input.lower():
                        results.append(f"Case Study: {c['title']} — {c['summary']}")
        except Exception as e:
            results.append(f"เกิดข้อผิดพลาดในการอ่าน cases.json: {e}")

    if results:
        return "\n".join(results)
    else:
        return "ไม่พบข้อมูล vendor หรือ case study ที่เกี่ยวข้อง"