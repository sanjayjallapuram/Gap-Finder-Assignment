import json
from services.llm_service import ask_llm,parse_json
from config.settings import TOPICS_PATH

# =========================================================
# 7. TOPIC MAPPING
# =========================================================

def build_topic_map(chunks):

    print("\nBuilding topic map...")

    syllabus_text = "\n".join(
        item.page_content
        for item in chunks
        if item.metadata.get("document_type") == "syllabus"
    )

    if not syllabus_text.strip():

        syllabus_text = "\n".join(
            item.page_content for item in chunks
        )

        print(
            "No syllabus-named PDF found. "
            "Inferring topics from available documents."
        )

    past_paper_text = "\n".join(
        item.page_content
        for item in chunks
        if item.metadata.get("document_type") == "past_paper"
    )

    prompt = f"""
    Create a topic map for a student's study materials.

    SYLLABUS:
    {syllabus_text[:10000]}

    PAST PAPERS:
    {past_paper_text[:10000]}

    Extract 4 to 12 important topics and their subtopics.

    Estimate exam_weight from 1 to 5:
    5 = frequently appearing in past papers.
    1 = low or unknown exam importance.

    Do not invent syllabus topics.
    If past papers are unavailable, use exam_weight 3.

    Return JSON in this format:

    {{
        "topics": [
            {{
                "name": "Topic name",
                "subtopics": ["Subtopic 1", "Subtopic 2"],
                "exam_weight": 3
            }}
        ]
    }}
    """

    response = ask_llm(prompt)

    topic_data = parse_json(response)

    topics = topic_data.get("topics", [])

    if not topics:
        raise ValueError("No topics extracted.")

    with open(TOPICS_PATH, "w", encoding="utf-8") as file:
        json.dump(topics, file, indent=4)

    print("\nExtracted Topics:")

    for topic in topics:
        print(
            f"- {topic['name']} "
            f"(Exam importance: {topic.get('exam_weight', 3)}/5)"
        )

    return topics


def load_topics():

    if not TOPICS_PATH.exists():
        raise FileNotFoundError(
            "Topic map missing. Run document ingestion first."
        )

    with open(TOPICS_PATH, encoding="utf-8") as file:
        return json.load(file)

