from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_auth import router as auth_router
from app.api.routes_transcript import router as transcript_router
app = FastAPI(title="YouTube Transcript API")
import sys
import os

# Add the parent directory to sys.path so Python can find ai
sys.path.append(r'D:\bfeduai\BruteForce_ai_part')
# import main_ai

# Now we can import main() from ai.main
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routes
app.include_router(auth_router)
app.include_router(transcript_router)
# import sys
# import os

# # Add the parent directory to sys.path so Python can find ai
# sys.path.append(r'D:\bfeduai\BruteForce_ai_part')
# import main_ai
# output = main_ai.main([{
#         "text": "यह वीडियो पूरी तरह से काल्पनिक है मतलब",
#         "starttime": 0.12,
#         "endtime": 4.4
#     },
#     {
#         "text": "इसमें जो कुछ भी दिखाया उसे प्लीज रियल",
#         "starttime": 2.76,
#         "endtime": 6.319
# #     }], user_question="question")
