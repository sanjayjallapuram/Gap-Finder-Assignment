from services.llm_service import ask_llm,parse_json
from services.rag_service import retrieve_context,format_context

# =========================================================
# 8. QUESTION GENERATION USING RAG
# =========================================================

def generate_questions(topic, number_of_questions=2):

    print(f"\nGenerating questions on topic: {topic['name']}")

    query = (
        topic["name"] + " " +
        " ".join(topic.get("subtopics", []))
    )

    retrieved_docs = retrieve_context(query, top_k=5)

    context = format_context(retrieved_docs)

    prompt = f"""
    Generate {number_of_questions} multiple-choice questions.

    TOPIC:
    {topic['name']}

    SUBTOPICS:
    {topic.get('subtopics', [])}

    RETRIEVED STUDY MATERIAL:
    {context}

    RULES:
    1. Questions must be based ONLY on retrieved material.
    2. Do not use external knowledge.
    3. Every question must have four options.
    4. Correct answer must be A, B, C or D.
    5. Include an explanation grounded in the material.
    6. Each question must specify a valid SOURCE_ID
       from the retrieved context above.
    7. If there is insufficient information, generate
       fewer questions rather than inventing facts.

    Return valid JSON:

    {{
        "questions": [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A",
                "explanation": "Explanation",
                "source_id": "S1"
            }}
        ]
    }}
    """

    response = ask_llm(prompt)

    question_data = parse_json(response)

    questions = []

    source_map = {
        doc["id"]: doc for doc in retrieved_docs
    }

    for question in question_data.get("questions", []):

        source = source_map.get(
            question.get("source_id")
        )

        if not source:
            continue

        answer = question.get("correct_answer", "").upper()

        options = question.get("options", {})

        if answer not in ["A", "B", "C", "D"]:
            continue

        if not all(
            key in options for key in ["A", "B", "C", "D"]
        ):
            continue

        question["topic"] = topic["name"]

        # Citation comes from actual retrieved metadata,
        # not from an unverified LLM-generated filename.

        question["citation"] = (
            f"{source['source']} | Page {source['page']}"
        )

        questions.append(question)

    return questions

