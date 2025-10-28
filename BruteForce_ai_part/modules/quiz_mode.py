# modules/quiz_mode.py

from modules.gemini_pipeline import process_watched_transcript
import json

def generate_quiz(transcript_chunks, num_questions=1):
    """
    Generates quiz questions and correct answers using Gemini.
    Handles transcript_chunks as a list of strings.
    """
    context_text = " ".join(transcript_chunks)  # <-- treat chunks as strings
    quiz_questions = []

    for _ in range(num_questions):
        prompt = (
            "From the given lecture transcript, generate one quiz question and its correct answer. "
            "Format the response as:\nQuestion: <question>\nAnswer: <answer>"
        )

        result = process_watched_transcript(context_text, user_question=prompt)
        full_text = result.get("answer", "")

        # Parse Gemini’s response
        if "Answer:" in full_text:
            parts = full_text.split("Answer:")
            question = parts[0].replace("Question:", "").strip()
            answer = parts[1].strip()
        else:
            question, answer = full_text.strip(), "Not provided"

        quiz_questions.append({"question": question, "answer": answer})

    return quiz_questions


def evaluate_answer_with_gemini(question, correct_answer, user_answer):
    """
    Uses Gemini to evaluate whether the user's answer is correct.
    Returns True if correct, False otherwise.
    """
    evaluation_prompt = (
        f"Question: {question}\n"
        f"Correct Answer: {correct_answer}\n"
        f"User Answer: {user_answer}\n\n"
        "Evaluate if the user's answer is correct based on meaning, not exact words. "
        "Respond ONLY in this JSON format: {\"verdict\": \"Correct\"} or {\"verdict\": \"Incorrect\"}."
    )

    result = process_watched_transcript("", user_question=evaluation_prompt)
    text = result.get("answer", "").strip()

    try:
        data = json.loads(text)
        return data.get("verdict", "").lower() == "correct"
    except json.JSONDecodeError:
        # fallback: if JSON parsing fails, assume incorrect
        return False


def run_quiz(transcript_chunks, num_questions=1):
    """
    Runs an AI-powered quiz session:
    - Gemini generates questions
    - User answers
    - Gemini evaluates correctness
    """
    print("🎯 Quiz Mode Activated!")
    quiz_questions = generate_quiz(transcript_chunks, num_questions=num_questions)
    user_results = []

    for q in quiz_questions:
        question = q["question"]
        correct_answer = q["answer"]

        print(f"\n❓ Question: {question}")
        user_answer = input("Your answer: ").strip()

        # Gemini evaluates the answer
        is_correct = evaluate_answer_with_gemini(question, correct_answer, user_answer)

        if is_correct:
            print("✅ Gemini says: Correct!\n")
        else:
            print(f"❌ Gemini says: Incorrect.\nCorrect Answer: {correct_answer}\n")

        user_results.append({
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    # Save results
    with open("quiz_results.json", "w", encoding="utf-8") as f:
        json.dump(user_results, f, indent=4, ensure_ascii=False)
    print("📁 Results saved to quiz_results.json")

    return user_results
