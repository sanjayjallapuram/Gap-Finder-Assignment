from services.topic_service import load_topics
from services.question_service import generate_questions
from database.db_manager import save_attempt
from collections import defaultdict


# =========================================================
# 9. DIAGNOSTIC QUIZ
# =========================================================

def conduct_quiz():

    topics = load_topics()

    all_questions = []

    print("\n========== DIAGNOSTIC QUIZ ==========")

    for topic in topics:

        questions = generate_questions(
            topic,
            number_of_questions=2
        )

        all_questions.extend(questions)

    if not all_questions:
        raise ValueError(
            "No questions generated. Check your documents."
        )

    print(
        f"\nTotal questions generated: {len(all_questions)}"
    )

    print("\nAnswer the following questions:\n")

    results = defaultdict(
        lambda: {"correct": 0, "total": 0, "mistakes": []}
    )

    for index, question in enumerate(all_questions, start=1):

        topic = question["topic"]

        print(f"\nQuestion {index}: {question['question']}")

        for key, value in question["options"].items():
            print(f"{key}. {value}")

        print(f"Source: {question['citation']}")

        answer = input(
            "\nYour answer (A/B/C/D): "
        ).strip().upper()

        while answer not in ["A", "B", "C", "D"]:

            answer = input(
                "Enter A, B, C or D: "
            ).strip().upper()

        correct_answer = question["correct_answer"]

        results[topic]["total"] += 1

        if answer == correct_answer:

            results[topic]["correct"] += 1

            print("\nCorrect answer!")

        else:

            results[topic]["mistakes"].append(
                question["question"]
            )

            print("\nIncorrect answer.")

        print(
            f"Correct answer: {correct_answer}"
        )

        print(
            f"Explanation: {question['explanation']}"
        )

    # Calculate topic-level scores.

    topic_scores = {}

    for topic, data in results.items():

        score = (
            data["correct"] / data["total"]
        ) * 100

        topic_scores[topic] = {
            "score": score,
            "correct": data["correct"],
            "total": data["total"],
            "mistakes": data["mistakes"]
        }

    save_attempt(topic_scores)

    return topic_scores
