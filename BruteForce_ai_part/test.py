test_chunks = [
    {"text": "Welcome back to the lecture. Today we will continue with stacks.", "starttime": 0.0, "endtime": 5.0},
    {"text": "A stack is a data structure that follows Last In, First Out, or LIFO principle.", "starttime": 5.0, "endtime": 12.0},
    {"text": "We can implement stacks using arrays or linked lists.", "starttime": 12.0, "endtime": 18.0}
]

# Example question
user_question = "Explain what a queue is and its principle."

# Call main_ai function
from main_ai import main
result = main(test_chunks, user_question)

print(result)
