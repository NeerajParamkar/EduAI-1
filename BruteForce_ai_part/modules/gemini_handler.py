import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question, context):
    prompt = f"""
You are an AI assistant that answers questions based strictly on the given lecture content. Use the content to generate clear, concise, and accurate answers in the language of the lecture (English or Hindi). 

Rules:
1. Answer in **Hindi** if the lecture is in Hindi; otherwise, use **English**. If the user explicitly asks for a different language, use that language.
2. Do not include unclear or verbatim transcript quotes unless they clarify the answer.
3. Provide answers that are **direct, explanatory, and easy to understand**.
4. Focus only on the relevant part of the lecture; avoid adding unrelated information.

    Use the following lecture content to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
