import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Try flash (fast) or pro (accurate)
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question, context):
    prompt = f"Use the following lecture content to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
