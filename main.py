import json
from groq import Groq

# Add your Groq API key here
client = Groq(api_key="your-groq-api-key-here")

system_prompt = """
You are an expert AI study assistant helping engineers
prepare for Gen AI job interviews at top tech companies.

RULES:
- Always be accurate. If unsure, say so clearly.
- Never make up facts or statistics.
- Keep explanations simple and practical.
- Always relate concepts to real world use cases.
"""

def ask_ai(prompt, temperature=0):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

def study_topic(topic):

    prompt1 = f"""
ROLE: Expert AI tutor
TASK: Explain {topic} for someone preparing for a Gen AI interview
FORMAT:
📖 EXPLANATION: [3 simple lines]
🌍 REAL WORLD EXAMPLE: [one practical example]

Think step by step before answering.
"""
    explanation = ask_ai(prompt1)

    prompt2 = f"""
ROLE: Senior Gen AI interviewer
TASK: Based on this explanation of {topic}:
{explanation}

Generate interview questions and answers.
FORMAT:
❓ INTERVIEW QUESTIONS:
1. [question]
2. [question]
3. [question]

✅ ANSWER TO QUESTION 1:
[2 line answer]
"""
    interview_prep = ask_ai(prompt2)

    prompt3 = f"""
Create a quiz question about {topic}.
Return ONLY this JSON. No extra text:
{{
    "question": "quiz question here",
    "options": {{
        "A": "option A",
        "B": "option B",
        "C": "option C",
        "D": "option D"
    }},
    "correct": "A or B or C or D",
    "explanation": "why this is correct in one line"
}}
"""
    quiz_raw = ask_ai(prompt3)

    try:
        quiz = json.loads(quiz_raw)
    except:
        start = quiz_raw.find('{')
        end = quiz_raw.rfind('}') + 1
        quiz = json.loads(quiz_raw[start:end])

    print("=" * 60)
    print(f"📚 TOPIC: {topic.upper()}")
    print("=" * 60)
    print(explanation)
    print()
    print(interview_prep)
    print()
    print("🧠 QUICK QUIZ:")
    print(f"Q: {quiz['question']}")
    for option, text in quiz['options'].items():
        print(f"   {option}) {text}")
    print(f"\n✅ Answer: {quiz['correct']}")
    print(f"💡 Why: {quiz['explanation']}")
    print("=" * 60)

# Run the assistant
topics = [
    "machine learning",
    "prompt engineering",
    "RAG - Retrieval Augmented Generation in Gen AI"
]

print("\n🤖 PERSONAL AI STUDY ASSISTANT")
print("Powered by Groq + LLaMA 3.1\n")

for topic in topics:
    study_topic(topic)
    print()
