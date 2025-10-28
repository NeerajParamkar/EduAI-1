# test_quiz.py
from main_ai import main

if __name__ == "__main__":
    transcript_path = r"C:\Users\ASUS\EduAI-1\BruteForce_ai_part\transcript_test.json"

    print("🚀 Starting AI Quiz Test...\n")

    # Run quiz mode (Gemini generates questions + checks answers)
    quiz_results = main(transcript_path, quiz_mode=True, num_quiz_questions=2)

    print("\n🧠 Quiz Results Summary:")
    for i, q in enumerate(quiz_results, 1):
        print(f"\n{i}. ❓ {q['question']}")
        print(f"   ➤ Your Answer: {q['user_answer']}")
        print(f"   ✅ Correct Answer: {q['correct_answer']}")
        print(f"   🎯 Correct: {'Yes' if q['is_correct'] else 'No'}")
