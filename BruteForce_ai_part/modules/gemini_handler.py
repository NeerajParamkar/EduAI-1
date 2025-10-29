import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv("")
# if not GEMINI_API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found in environment")

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question, context):
    prompt = f"""
You are an AI assistant that answers questions based strictly on the given lecture content. Use the content to generate clear, concise, and accurate answers in the language of the lecture (English or Hindi). 

Rules:
1. DEFAULT LANGUAGE IS ENGLISH.IF USER ASKS TO EXPLAIN IN HINDI THEN USE HINDI. 
2. Do not include unclear or verbatim transcript quotes unless they clarify the answer.
3. Provide answers that are **direct, explanatory, and easy to understand**.
4. Focus only on the relevant part of the lecture; avoid adding unrelated information.

    Use the following lecture content to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
