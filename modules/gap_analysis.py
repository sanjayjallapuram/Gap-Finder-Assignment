from services.topic_service import load_topics
import json
from config.settings import REPORT_PATH

# =========================================================
# 10. GAP ANALYSIS
# =========================================================

def analyze_gaps(topic_scores):

    topics = load_topics()

    topic_metadata = {
        topic["name"]: topic for topic in topics
    }

    report = {}

    print("\n========== GAP ANALYSIS REPORT ==========")

    for topic, data in topic_scores.items():

        score = data["score"]

        if score < 50:
            status = "WEAK"

        elif score < 75:
            status = "MEDIUM"

        else:
            status = "STRONG"

        exam_weight = topic_metadata.get(
            topic, {}
        ).get("exam_weight", 3)

        priority = (
            0.7 * (100 - score) +
            0.3 * (exam_weight * 20)
        )

        report[topic] = {
            **data,
            "status": status,
            "exam_weight": exam_weight,
            "priority": priority
        }

        print(f"\nTopic: {topic}")
        print(f"Score: {score:.1f}%")
        print(f"Status: {status}")
        print(f"Exam importance: {exam_weight}/5")

        if data["mistakes"]:

            print("Reason for weakness:")

            for mistake in data["mistakes"]:
                print(f"- Incorrect response: {mistake}")

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report


def load_report():
    if not REPORT_PATH.exists():
        return None
    with open(REPORT_PATH, encoding="utf-8") as file:
        return json.load(file)
