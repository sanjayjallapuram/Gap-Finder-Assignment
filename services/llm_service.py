from config.settings import client,MODEL
import json


# =========================================================
# 3. LLM HELPER
# =========================================================


def ask_llm(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are GapFinder AI, an educational "
                    "assessment assistant. Follow the user's "
                    "instructions strictly. Return valid JSON "
                    "when JSON is requested. Never invent "
                    "information beyond supplied context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=4000
    )

    return response.choices[0].message.content


def parse_json(response):

    response = response.strip()

    if response.startswith("```"):
        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0]

    return json.loads(response)
