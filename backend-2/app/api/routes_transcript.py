from fastapi import APIRouter, Depends, HTTPException
from app.db.database import transcripts_collection
database_collection = transcripts_collection
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import json
from urllib.parse import urlparse, parse_qs
from fastapi.responses import JSONResponse
from app.db.database import chat_collection
from datetime import datetime
import time
import asyncio
import sys
import os

sys.path.append(r'D:\bfeduai\BruteForce_ai_part')
import main_ai
import modules.tts_handler
router = APIRouter(prefix="/transcript", tags=["Transcript"])

class VideoRequest(BaseModel):
    video_id: str

class UrlData(BaseModel):
    url: str

class TranscriptTimeRange(BaseModel):
    video_id: str
    start_time: float
    end_time: float

class ChatRequest(BaseModel):
    video_id: str
    question: str
def get_youtube_id(url):
    """
    Extracts the YouTube video ID from a URL.
    Works for both long and short YouTube links.
    """
    parsed_url = urlparse(url)
    
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]
    
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')
    
    else:
        return None

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import json
tc=[
    {
        "text": "so we will be continuing with our stack",
        "starttime": 3.32,
        "endtime": 7.04
    },
    {
        "text": "and Q playlist we starting off hey we",
        "starttime": 4.839,
        "endtime": 8.32
    },
    {
        "text": "welcome back to the channel I hope you",
        "starttime": 7.04,
        "endtime": 10.16
    },
    {
        "text": "guys are doing extremely well so the",
        "starttime": 8.32,
        "endtime": 12.759
    },
    {
        "text": "problem that we will be solving today is",
        "starttime": 10.16,
        "endtime": 15.4
    },
    {
        "text": "balanced parenthesis so what is the",
        "starttime": 12.759,
        "endtime": 17.8
    },
    {
        "text": "problem statement is stating that you",
        "starttime": 15.4,
        "endtime": 19.92
    },
    {
        "text": "will be given a string and it will only",
        "starttime": 17.8,
        "endtime": 22.039
    },
    {
        "text": "be containing characters like the",
        "starttime": 19.92,
        "endtime": 24.080000000000002
    },
    {
        "text": "brackets now these are the possible",
        "starttime": 22.039,
        "endtime": 27.560000000000002
    },
    {
        "text": "brackets that it might contain now your",
        "starttime": 24.08,
        "endtime": 30.479999999999997
    },
    {
        "text": "task is to check if the given string is",
        "starttime": 27.56,
        "endtime": 33.399
    },
    {
        "text": "a balanced parenthesis string or not",
        "starttime": 30.48,
        "endtime": 35.0
    },
    {
        "text": "what are the conditions it should follow",
        "starttime": 33.399,
        "endtime": 36.84
    },
    {
        "text": "to be called a balanced parenthesis",
        "starttime": 35.0,
        "endtime": 39.879
    },
    {
        "text": "string first one is every opening",
        "starttime": 36.84,
        "endtime": 43.399
    },
    {
        "text": "bracket should have a same closing",
        "starttime": 39.879,
        "endtime": 47.0
    },
    {
        "text": "bracket got it every closing bracket",
        "starttime": 43.399,
        "endtime": 49.92
    },
    {
        "text": "should have a same opening bracket the",
        "starttime": 47.0,
        "endtime": 51.559
    },
    {
        "text": "other examples will be",
        "starttime": 49.92,
        "endtime": 54.28
    },
    {
        "text": "this and this",
        "starttime": 51.559,
        "endtime": 57.48
    },
    {
        "text": "one got it and the third one is it",
        "starttime": 54.28,
        "endtime": 60.760000000000005
    },
    {
        "text": "should follow the order as well",
        "starttime": 57.48,
        "endtime": 63.31999999999999
    },
    {
        "text": "let's understand the three conditions so",
        "starttime": 60.76,
        "endtime": 65.75999999999999
    },
    {
        "text": "if I look at this particular example",
        "starttime": 63.32,
        "endtime": 68.32
    },
    {
        "text": "let's check if this is balanced or not",
        "starttime": 65.76,
        "endtime": 70.43900000000001
    },
    {
        "text": "now first I'm I'm seeing an opening",
        "starttime": 68.32,
        "endtime": 72.27999999999999
    },
    {
        "text": "bracket and after that I'm seeing a",
        "starttime": 70.439,
        "endtime": 74.55999999999999
    },
    {
        "text": "closing bracket so they're following the",
        "starttime": 72.28,
        "endtime": 77.92
    },
    {
        "text": "order and they're of the same type so",
        "starttime": 74.56,
        "endtime": 81.0
    },
    {
        "text": "opening and then closing perfect after",
        "starttime": 77.92,
        "endtime": 83.479
    },
    {
        "text": "that there is an opening after that",
        "starttime": 81.0,
        "endtime": 85.52
    },
    {
        "text": "there is an opening after that there is",
        "starttime": 83.479,
        "endtime": 88.119
    },
    {
        "text": "a closing so for this closing for this",
        "starttime": 85.52,
        "endtime": 91.24
    },
    {
        "text": "closing I have a corresponding opening",
        "starttime": 88.119,
        "endtime": 93.2
    },
    {
        "text": "right before it so they're following the",
        "starttime": 91.24,
        "endtime": 96.079
    },
    {
        "text": "order as well and they're of the same",
        "starttime": 93.2,
        "endtime": 99.759
    },
    {
        "text": "type as well perfect after this I have",
        "starttime": 96.079,
        "endtime": 102.24
    },
    {
        "text": "this one and then there is a closing so",
        "starttime": 99.759,
        "endtime": 104.399
    },
    {
        "text": "for this closing I have a corresponding",
        "starttime": 102.24,
        "endtime": 106.79899999999999
    },
    {
        "text": "opening so they are following the order",
        "starttime": 104.399,
        "endtime": 108.719
    },
    {
        "text": "got it so they have followed the order",
        "starttime": 106.799,
        "endtime": 110.52000000000001
    },
    {
        "text": "and they have also followed the order",
        "starttime": 108.719,
        "endtime": 113.6
    },
    {
        "text": "now I have a closing for this I have a",
        "starttime": 110.52,
        "endtime": 116.19999999999999
    },
    {
        "text": "opening as well so they are also",
        "starttime": 113.6,
        "endtime": 118.52
    },
    {
        "text": "following the order so every bracket has",
        "starttime": 116.2,
        "endtime": 120.28
    },
    {
        "text": "a similar kind of bracket that is",
        "starttime": 118.52,
        "endtime": 122.28
    },
    {
        "text": "closing itself and they're following the",
        "starttime": 120.28,
        "endtime": 125.32000000000001
    },
    {
        "text": "order as well so this can be called as a",
        "starttime": 122.28,
        "endtime": 128.479
    },
    {
        "text": "balanced parenthesis got it whereas if I",
        "starttime": 125.32,
        "endtime": 131.239
    },
    {
        "text": "look at this particular example this is",
        "starttime": 128.479,
        "endtime": 133.84
    },
    {
        "text": "an opening this is a closing so they are",
        "starttime": 131.239,
        "endtime": 136.64000000000001
    },
    {
        "text": "following the Order Perfect this is a",
        "starttime": 133.84,
        "endtime": 139.28
    },
    {
        "text": "opening this is a opening this is a",
        "starttime": 136.64,
        "endtime": 142.16
    },
    {
        "text": "closing so they are following the order",
        "starttime": 139.28,
        "endtime": 144.56
    },
    {
        "text": "after that this is a opening but this is",
        "starttime": 142.16,
        "endtime": 148.319
    },
    {
        "text": "a closing and this is not following the",
        "starttime": 144.56,
        "endtime": 151.72
    },
    {
        "text": "order they are not following the order",
        "starttime": 148.319,
        "endtime": 154.2
    },
    {
        "text": "thereby this is not a balanced",
        "starttime": 151.72,
        "endtime": 156.959
    },
    {
        "text": "parenthesis let's look at other examples",
        "starttime": 154.2,
        "endtime": 159.51899999999998
    },
    {
        "text": "so if I take an example like this now",
        "starttime": 156.959,
        "endtime": 162.599
    },
    {
        "text": "this is also not a balanced parenthesis",
        "starttime": 159.519,
        "endtime": 165.159
    },
    {
        "text": "why now they are following the order for",
        "starttime": 162.599,
        "endtime": 167.67999999999998
    },
    {
        "text": "this opening there is a closing but for",
        "starttime": 165.159,
        "endtime": 170.84
    },
    {
        "text": "this opening there is no closing thereby",
        "starttime": 167.68,
        "endtime": 173.4
    },
    {
        "text": "I said for every opening there must be a",
        "starttime": 170.84,
        "endtime": 175.879
    },
    {
        "text": "closing and vice versa if I take a",
        "starttime": 173.4,
        "endtime": 178.59900000000002
    },
    {
        "text": "string like this this is also not",
        "starttime": 175.879,
        "endtime": 181.319
    },
    {
        "text": "balanced because for every closing there",
        "starttime": 178.599,
        "endtime": 184.319
    },
    {
        "text": "is not an opening got it and this",
        "starttime": 181.319,
        "endtime": 186.319
    },
    {
        "text": "describes the order so these are the",
        "starttime": 184.319,
        "endtime": 187.83999999999997
    },
    {
        "text": "three conditions that you have to keep",
        "starttime": 186.319,
        "endtime": 190.92
    },
    {
        "text": "in mind if calling someone as a balanced",
        "starttime": 187.84,
        "endtime": 195.84
    },
    {
        "text": "parenthesis if you carefully look what",
        "starttime": 190.92,
        "endtime": 197.83999999999997
    },
    {
        "text": "do we need to solve now there are two",
        "starttime": 195.84,
        "endtime": 201.08
    },
    {
        "text": "things whenever I'm getting a closing",
        "starttime": 197.84,
        "endtime": 205.239
    },
    {
        "text": "bracket I'm checking out if the last",
        "starttime": 201.08,
        "endtime": 208.56
    },
    {
        "text": "opening that I saw the last opening that",
        "starttime": 205.239,
        "endtime": 213.04
    },
    {
        "text": "I saw is a my type is of my type that's",
        "starttime": 208.56,
        "endtime": 215.879
    },
    {
        "text": "what I'm checking right so what am I",
        "starttime": 213.04,
        "endtime": 220.239
    },
    {
        "text": "looking for I'm looking for last",
        "starttime": 215.879,
        "endtime": 222.2
    },
    {
        "text": "opening",
        "starttime": 220.239,
        "endtime": 224.519
    },
    {
        "text": "encountered that's",
        "starttime": 222.2,
        "endtime": 227.83999999999997
    },
    {
        "text": "it whenever I encounter an closing",
        "starttime": 224.519,
        "endtime": 230.64000000000001
    },
    {
        "text": "bracket I look for the last opening that",
        "starttime": 227.84,
        "endtime": 234.599
    },
    {
        "text": "I encountered correct okay so it kind of",
        "starttime": 230.64,
        "endtime": 236.48
    },
    {
        "text": "gives me an idea I'm looking for the",
        "starttime": 234.599,
        "endtime": 239.28
    },
    {
        "text": "last opening encountered so I just need",
        "starttime": 236.48,
        "endtime": 242.23899999999998
    },
    {
        "text": "to preserve the opening brackets that is",
        "starttime": 239.28,
        "endtime": 244.36
    },
    {
        "text": "the first thing that should come to my",
        "starttime": 242.239,
        "endtime": 246.519
    },
    {
        "text": "mind that I will be preserving all the",
        "starttime": 244.36,
        "endtime": 249.68
    },
    {
        "text": "opening brackets and the other thing is",
        "starttime": 246.519,
        "endtime": 252.64000000000001
    },
    {
        "text": "I should be able to see the last one so",
        "starttime": 249.68,
        "endtime": 256.32
    },
    {
        "text": "which data structure yes stack because",
        "starttime": 252.64,
        "endtime": 258.4
    },
    {
        "text": "that is going to tell me the last one",
        "starttime": 256.32,
        "endtime": 260.639
    },
    {
        "text": "because it follows a last in first out",
        "starttime": 258.4,
        "endtime": 263.0
    },
    {
        "text": "mechanism if you keep something in the",
        "starttime": 260.639,
        "endtime": 264.96000000000004
    },
    {
        "text": "data structure and you want to check out",
        "starttime": 263.0,
        "endtime": 266.52
    },
    {
        "text": "which one was the last thing that you",
        "starttime": 264.96,
        "endtime": 270.0
    },
    {
        "text": "kept that's where stack comes in got it",
        "starttime": 266.52,
        "endtime": 272.24
    },
    {
        "text": "so what I will be doing is I'll be doing",
        "starttime": 270.0,
        "endtime": 274.919
    },
    {
        "text": "a dryon using the stack data structure",
        "starttime": 272.24,
        "endtime": 277.12
    },
    {
        "text": "so let's take the stack data structure",
        "starttime": 274.919,
        "endtime": 280.52
    },
    {
        "text": "so this is my stack data structure now",
        "starttime": 277.12,
        "endtime": 282.72
    },
    {
        "text": "at the opening bracket we need to",
        "starttime": 280.52,
        "endtime": 284.919
    },
    {
        "text": "preserve the openings so I'll just",
        "starttime": 282.72,
        "endtime": 287.56
    },
    {
        "text": "preserve this opening after this I'll go",
        "starttime": 284.919,
        "endtime": 290.639
    },
    {
        "text": "to the next one now this is a closing",
        "starttime": 287.56,
        "endtime": 292.68
    },
    {
        "text": "bracket whenever you get a closing",
        "starttime": 290.639,
        "endtime": 295.16
    },
    {
        "text": "bracket you take out the top element",
        "starttime": 292.68,
        "endtime": 297.12
    },
    {
        "text": "from the stack you take out the top",
        "starttime": 295.16,
        "endtime": 300.32000000000005
    },
    {
        "text": "element from the stack and you compare",
        "starttime": 297.12,
        "endtime": 302.28000000000003
    },
    {
        "text": "with the current closing are they of the",
        "starttime": 300.32,
        "endtime": 304.84
    },
    {
        "text": "similar types you say yes and you're",
        "starttime": 302.28,
        "endtime": 307.19899999999996
    },
    {
        "text": "fine you can move ahead again you get an",
        "starttime": 304.84,
        "endtime": 309.88
    },
    {
        "text": "opening you have to preserve them so you",
        "starttime": 307.199,
        "endtime": 312.0
    },
    {
        "text": "preserve it in your stack you preserve",
        "starttime": 309.88,
        "endtime": 314.24
    },
    {
        "text": "it in your stack after that you get",
        "starttime": 312.0,
        "endtime": 318.44
    },
    {
        "text": "another opening again you preserve",
        "starttime": 314.24,
        "endtime": 321.72
    },
    {
        "text": "it in your stack after that you again",
        "starttime": 318.44,
        "endtime": 324.039
    },
    {
        "text": "get a closing this time when you getting",
        "starttime": 321.72,
        "endtime": 326.8
    },
    {
        "text": "a closing what you will do is you will",
        "starttime": 324.039,
        "endtime": 328.639
    },
    {
        "text": "head over and get the",
        "starttime": 326.8,
        "endtime": 332.36
    },
    {
        "text": "last opening that you had and you see",
        "starttime": 328.639,
        "endtime": 335.56
    },
    {
        "text": "that they're matching fine after that",
        "starttime": 332.36,
        "endtime": 338.199
    },
    {
        "text": "you get again an opening so you take it",
        "starttime": 335.56,
        "endtime": 341.0
    },
    {
        "text": "after that you get a closing so you take",
        "starttime": 338.199,
        "endtime": 342.88
    },
    {
        "text": "that closing and you head over to the",
        "starttime": 341.0,
        "endtime": 345.68
    },
    {
        "text": "stack you take out from it and you see",
        "starttime": 342.88,
        "endtime": 348.12
    },
    {
        "text": "that they are matching and if they're",
        "starttime": 345.68,
        "endtime": 350.6
    },
    {
        "text": "matching it's fine after that you get to",
        "starttime": 348.12,
        "endtime": 353.72
    },
    {
        "text": "the last one it's a closing bracket and",
        "starttime": 350.6,
        "endtime": 355.759
    },
    {
        "text": "if it is a closing one again you go to",
        "starttime": 353.72,
        "endtime": 358.96000000000004
    },
    {
        "text": "the stack and you see hey stack what is",
        "starttime": 355.759,
        "endtime": 361.16
    },
    {
        "text": "the last one he says this one oh you're",
        "starttime": 358.96,
        "endtime": 363.19899999999996
    },
    {
        "text": "matching perfect and after that the",
        "starttime": 361.16,
        "endtime": 366.16
    },
    {
        "text": "iteration is over and you see that the",
        "starttime": 363.199,
        "endtime": 369.199
    },
    {
        "text": "stack is empty what does it mean for",
        "starttime": 366.16,
        "endtime": 372.0
    },
    {
        "text": "every opening for every opening that I",
        "starttime": 369.199,
        "endtime": 375.039
    },
    {
        "text": "preserved I got a corresponding closing",
        "starttime": 372.0,
        "endtime": 377.479
    },
    {
        "text": "so thereby I can say that this",
        "starttime": 375.039,
        "endtime": 380.52
    },
    {
        "text": "particular string is a Balan string got",
        "starttime": 377.479,
        "endtime": 384.75899999999996
    },
    {
        "text": "it perfect now what I will do is I'll",
        "starttime": 380.52,
        "endtime": 387.52
    },
    {
        "text": "now do the same iteration over the",
        "starttime": 384.759,
        "endtime": 389.68
    },
    {
        "text": "second string to understand how do we",
        "starttime": 387.52,
        "endtime": 391.56
    },
    {
        "text": "figure out that it is",
        "starttime": 389.68,
        "endtime": 394.199
    },
    {
        "text": "unbalanced again we can start from here",
        "starttime": 391.56,
        "endtime": 395.88
    },
    {
        "text": "maybe I can I can take a stack so that",
        "starttime": 394.199,
        "endtime": 398.08
    },
    {
        "text": "we understand it in a much better way",
        "starttime": 395.88,
        "endtime": 400.199
    },
    {
        "text": "perfect I've taken a stack first one is",
        "starttime": 398.08,
        "endtime": 402.8
    },
    {
        "text": "an opening one so I preserve it after",
        "starttime": 400.199,
        "endtime": 405.68
    },
    {
        "text": "that I go to the next one now this is a",
        "starttime": 402.8,
        "endtime": 407.72
    },
    {
        "text": "closing bracket so whenever it's a",
        "starttime": 405.68,
        "endtime": 410.039
    },
    {
        "text": "closing bracket I get the top of the",
        "starttime": 407.72,
        "endtime": 412.68
    },
    {
        "text": "stack I get the top of the stack and I",
        "starttime": 410.039,
        "endtime": 414.639
    },
    {
        "text": "see that they're matching I see that",
        "starttime": 412.68,
        "endtime": 416.68
    },
    {
        "text": "they're matching so it's fine again I go",
        "starttime": 414.639,
        "endtime": 419.0
    },
    {
        "text": "to this one it's an opening so I'll take",
        "starttime": 416.68,
        "endtime": 421.879
    },
    {
        "text": "it off after that again it's an opening",
        "starttime": 419.0,
        "endtime": 425.0
    },
    {
        "text": "so I'll take it off this time it's a",
        "starttime": 421.879,
        "endtime": 427.96000000000004
    },
    {
        "text": "closing whenever it's a closing I go",
        "starttime": 425.0,
        "endtime": 430.039
    },
    {
        "text": "back to the stack and I take out the",
        "starttime": 427.96,
        "endtime": 433.31899999999996
    },
    {
        "text": "closing and I match and it's a match",
        "starttime": 430.039,
        "endtime": 435.759
    },
    {
        "text": "again it's it's a opening so I take it",
        "starttime": 433.319,
        "endtime": 438.8
    },
    {
        "text": "off next time it's a closing so you go",
        "starttime": 435.759,
        "endtime": 440.199
    },
    {
        "text": "to the stack and say which is the last",
        "starttime": 438.8,
        "endtime": 442.24
    },
    {
        "text": "scene so it gives you this one and you",
        "starttime": 440.199,
        "endtime": 445.40000000000003
    },
    {
        "text": "say it's a m match and if it is a mess",
        "starttime": 442.24,
        "endtime": 447.84000000000003
    },
    {
        "text": "match you're done and dusted yes you're",
        "starttime": 445.4,
        "endtime": 449.96
    },
    {
        "text": "done and dusted so so it's very",
        "starttime": 447.84,
        "endtime": 453.28
    },
    {
        "text": "important to preserve the opening one to",
        "starttime": 449.96,
        "endtime": 455.15999999999997
    },
    {
        "text": "figure out which was the last one",
        "starttime": 453.28,
        "endtime": 457.96
    },
    {
        "text": "because every opening should have a",
        "starttime": 455.16,
        "endtime": 460.28000000000003
    },
    {
        "text": "corresponding closing and in the same",
        "starttime": 457.96,
        "endtime": 462.12
    },
    {
        "text": "order and the same order that is very",
        "starttime": 460.28,
        "endtime": 465.23999999999995
    },
    {
        "text": "very important understood uh some other",
        "starttime": 462.12,
        "endtime": 467.68
    },
    {
        "text": "cases if you want to do a super quick",
        "starttime": 465.24,
        "endtime": 470.919
    },
    {
        "text": "dry run some other cases would be let's",
        "starttime": 467.68,
        "endtime": 472.879
    },
    {
        "text": "say you take a string which is opening",
        "starttime": 470.919,
        "endtime": 475.75899999999996
    },
    {
        "text": "opening and closing and then I take a",
        "starttime": 472.879,
        "endtime": 478.28000000000003
    },
    {
        "text": "stack first one I have opening so you",
        "starttime": 475.759,
        "endtime": 480.36
    },
    {
        "text": "can put that in then I again have",
        "starttime": 478.28,
        "endtime": 481.919
    },
    {
        "text": "opening so you can put that in then",
        "starttime": 480.36,
        "endtime": 483.47900000000004
    },
    {
        "text": "again I have a closing so for this",
        "starttime": 481.919,
        "endtime": 485.96
    },
    {
        "text": "closing you'll get this one which is",
        "starttime": 483.479,
        "endtime": 488.24
    },
    {
        "text": "typically matching and after that the",
        "starttime": 485.96,
        "endtime": 490.96
    },
    {
        "text": "iteration is over but the stack still",
        "starttime": 488.24,
        "endtime": 494.12
    },
    {
        "text": "has an opening bracket which means every",
        "starttime": 490.96,
        "endtime": 497.35999999999996
    },
    {
        "text": "opening did not get a closing got it",
        "starttime": 494.12,
        "endtime": 499.24
    },
    {
        "text": "same might happen for something like",
        "starttime": 497.36,
        "endtime": 502.36
    },
    {
        "text": "this where you're just closing in that",
        "starttime": 499.24,
        "endtime": 503.759
    },
    {
        "text": "scenario",
        "starttime": 502.36,
        "endtime": 506.40000000000003
    },
    {
        "text": "whenever you have a stack and you",
        "starttime": 503.759,
        "endtime": 509.0
    },
    {
        "text": "encounter a closing bracket the stack",
        "starttime": 506.4,
        "endtime": 511.87899999999996
    },
    {
        "text": "will be M that means you don't have a",
        "starttime": 509.0,
        "endtime": 514.479
    },
    {
        "text": "corresponding opening for the closing so",
        "starttime": 511.879,
        "endtime": 518.64
    },
    {
        "text": "this is also unbalanced got it so time",
        "starttime": 514.479,
        "endtime": 520.479
    },
    {
        "text": "to write down the pseudo code again",
        "starttime": 518.64,
        "endtime": 521.8
    },
    {
        "text": "super simple we're going to write the",
        "starttime": 520.479,
        "endtime": 524.08
    },
    {
        "text": "function just going to return a bullion",
        "starttime": 521.8,
        "endtime": 526.4799999999999
    },
    {
        "text": "stating true or false if it is balanced",
        "starttime": 524.08,
        "endtime": 529.32
    },
    {
        "text": "or unbalanced respectively so I'll be",
        "starttime": 526.48,
        "endtime": 531.16
    },
    {
        "text": "getting a",
        "starttime": 529.32,
        "endtime": 534.6400000000001
    },
    {
        "text": "string first thing we need a stack so",
        "starttime": 531.16,
        "endtime": 537.16
    },
    {
        "text": "maybe I'll be defining a stack so we",
        "starttime": 534.64,
        "endtime": 539.04
    },
    {
        "text": "stack s again depending on the",
        "starttime": 537.16,
        "endtime": 540.399
    },
    {
        "text": "programming language you're using you",
        "starttime": 539.04,
        "endtime": 542.88
    },
    {
        "text": "can Define the stack stack will be",
        "starttime": 540.399,
        "endtime": 545.6
    },
    {
        "text": "storing characters so maybe I can",
        "starttime": 542.88,
        "endtime": 547.72
    },
    {
        "text": "iterate over the string so assuming the",
        "starttime": 545.6,
        "endtime": 549.8000000000001
    },
    {
        "text": "String's length is n we can iterate till",
        "starttime": 547.72,
        "endtime": 552.8000000000001
    },
    {
        "text": "n minus one at index we know one thing",
        "starttime": 549.8,
        "endtime": 555.04
    },
    {
        "text": "if it is an opening bracket and the",
        "starttime": 552.8,
        "endtime": 558.76
    },
    {
        "text": "opening bracket will only be S of I",
        "starttime": 555.04,
        "endtime": 561.079
    },
    {
        "text": "equal to equal to",
        "starttime": 558.76,
        "endtime": 568.56
    },
    {
        "text": "this or S of I equal to equal to this or",
        "starttime": 561.079,
        "endtime": 571.399
    },
    {
        "text": "S of I equal to equal",
        "starttime": 568.56,
        "endtime": 575.1199999999999
    },
    {
        "text": "to this so that's the case you ask the",
        "starttime": 571.399,
        "endtime": 577.92
    },
    {
        "text": "stack hey stack can you store this one",
        "starttime": 575.12,
        "endtime": 580.2
    },
    {
        "text": "and the stack is going to store it",
        "starttime": 577.92,
        "endtime": 583.12
    },
    {
        "text": "perfect now the logic comes up whenever",
        "starttime": 580.2,
        "endtime": 585.5600000000001
    },
    {
        "text": "it's a closing bracket if it's a closing",
        "starttime": 583.12,
        "endtime": 587.92
    },
    {
        "text": "bracket at at any moment the stack is",
        "starttime": 585.56,
        "endtime": 592.2399999999999
    },
    {
        "text": "empty that means it doesn't have a",
        "starttime": 587.92,
        "endtime": 594.92
    },
    {
        "text": "corresponding it doesn't have a",
        "starttime": 592.24,
        "endtime": 597.279
    },
    {
        "text": "corresponding opening bracket for itself",
        "starttime": 594.92,
        "endtime": 598.959
    },
    {
        "text": "so you can just break out and return",
        "starttime": 597.279,
        "endtime": 600.4399999999999
    },
    {
        "text": "false",
        "starttime": 598.959,
        "endtime": 602.64
    },
    {
        "text": "otherwise what we will be doing is",
        "starttime": 600.44,
        "endtime": 605.8000000000001
    },
    {
        "text": "inside the else we'll be like okay the",
        "starttime": 602.64,
        "endtime": 607.68
    },
    {
        "text": "stack has something maybe I can just get",
        "starttime": 605.8,
        "endtime": 611.3599999999999
    },
    {
        "text": "out that element we can say character CH",
        "starttime": 607.68,
        "endtime": 614.64
    },
    {
        "text": "equal to St do top so you get the top",
        "starttime": 611.36,
        "endtime": 616.6800000000001
    },
    {
        "text": "and then you can pop it out because this",
        "starttime": 614.64,
        "endtime": 619.1999999999999
    },
    {
        "text": "will be required for comparison we know",
        "starttime": 616.68,
        "endtime": 622.64
    },
    {
        "text": "one thing it has to meet three",
        "starttime": 619.2,
        "endtime": 626.44
    },
    {
        "text": "conditions if s of I is equal to equal",
        "starttime": 622.64,
        "endtime": 629.16
    },
    {
        "text": "to the my bad it's a closing one so if",
        "starttime": 626.44,
        "endtime": 632.2790000000001
    },
    {
        "text": "this this is the closing one then the",
        "starttime": 629.16,
        "endtime": 634.519
    },
    {
        "text": "character that I got from the stack has",
        "starttime": 632.279,
        "endtime": 636.68
    },
    {
        "text": "to be the corresponding opening one has",
        "starttime": 634.519,
        "endtime": 638.24
    },
    {
        "text": "to be the corresponding opening one",
        "starttime": 636.68,
        "endtime": 640.3599999999999
    },
    {
        "text": "perfect so either this condition should",
        "starttime": 638.24,
        "endtime": 645.04
    },
    {
        "text": "be met or or I should be like s of I is",
        "starttime": 640.36,
        "endtime": 647.32
    },
    {
        "text": "equal to equal to if it is this",
        "starttime": 645.04,
        "endtime": 649.68
    },
    {
        "text": "particular closing then the character",
        "starttime": 647.32,
        "endtime": 653.8000000000001
    },
    {
        "text": "should be this particular opening or or",
        "starttime": 649.68,
        "endtime": 657.1999999999999
    },
    {
        "text": "for the third bracket if it is not",
        "starttime": 653.8,
        "endtime": 659.88
    },
    {
        "text": "matching if it is not matching in that",
        "starttime": 657.2,
        "endtime": 662.0
    },
    {
        "text": "scenario you go to the this particular",
        "starttime": 659.88,
        "endtime": 666.0
    },
    {
        "text": "if else and you return a false if this",
        "starttime": 662.0,
        "endtime": 668.48
    },
    {
        "text": "particular if is matching well and good",
        "starttime": 666.0,
        "endtime": 670.24
    },
    {
        "text": "otherwise you return of false and the",
        "starttime": 668.48,
        "endtime": 673.04
    },
    {
        "text": "fall Loop ends and at the end of the day",
        "starttime": 670.24,
        "endtime": 676.6800000000001
    },
    {
        "text": "you say return stack. empty if the stack",
        "starttime": 673.04,
        "endtime": 678.12
    },
    {
        "text": "is empty that means everything is",
        "starttime": 676.68,
        "endtime": 680.1999999999999
    },
    {
        "text": "matched but the stack still has some",
        "starttime": 678.12,
        "endtime": 682.399
    },
    {
        "text": "opening brackets that means it didn't",
        "starttime": 680.2,
        "endtime": 685.0
    },
    {
        "text": "find it corresponding closing brackets",
        "starttime": 682.399,
        "endtime": 687.92
    },
    {
        "text": "that's it that will be it if I have to",
        "starttime": 685.0,
        "endtime": 690.72
    },
    {
        "text": "discuss the time complexity what will",
        "starttime": 687.92,
        "endtime": 693.24
    },
    {
        "text": "that be I'm just iterating over so",
        "starttime": 690.72,
        "endtime": 695.12
    },
    {
        "text": "that's a beo",
        "starttime": 693.24,
        "endtime": 699.16
    },
    {
        "text": "of N and what about the space complexity",
        "starttime": 695.12,
        "endtime": 701.32
    },
    {
        "text": "I'm using the stack data structure at",
        "starttime": 699.16,
        "endtime": 703.4399999999999
    },
    {
        "text": "the worst case if everything is an",
        "starttime": 701.32,
        "endtime": 704.9200000000001
    },
    {
        "text": "opening bracket I'm going to store",
        "starttime": 703.44,
        "endtime": 706.519
    },
    {
        "text": "everything out I'm going to store",
        "starttime": 704.92,
        "endtime": 708.56
    },
    {
        "text": "everything out this will be the time",
        "starttime": 706.519,
        "endtime": 711.639
    },
    {
        "text": "complexity and the space complexity can",
        "starttime": 708.56,
        "endtime": 714.1999999999999
    },
    {
        "text": "we make it better no because we'll have",
        "starttime": 711.639,
        "endtime": 716.72
    },
    {
        "text": "to match uh for every corresponding",
        "starttime": 714.2,
        "endtime": 718.1600000000001
    },
    {
        "text": "opening there should be a corresponding",
        "starttime": 716.72,
        "endtime": 720.6800000000001
    },
    {
        "text": "closing so we need to store it somewhere",
        "starttime": 718.16,
        "endtime": 723.12
    },
    {
        "text": "to have a match got it so the space",
        "starttime": 720.68,
        "endtime": 725.4799999999999
    },
    {
        "text": "complexity cannot be improved so this",
        "starttime": 723.12,
        "endtime": 727.2
    },
    {
        "text": "will wait for this one so if you're",
        "starttime": 725.48,
        "endtime": 728.36
    },
    {
        "text": "still now watching and if you've",
        "starttime": 727.2,
        "endtime": 730.24
    },
    {
        "text": "understood everything please please do",
        "starttime": 728.36,
        "endtime": 731.519
    },
    {
        "text": "consider giving us a like and if you're",
        "starttime": 730.24,
        "endtime": 733.0790000000001
    },
    {
        "text": "new to our channel do consider",
        "starttime": 731.519,
        "endtime": 735.199
    },
    {
        "text": "subscribing to us as well with this I'll",
        "starttime": 733.079,
        "endtime": 736.5999999999999
    },
    {
        "text": "be wrapping up this video let's meet in",
        "starttime": 735.199,
        "endtime": 739.959
    },
    {
        "text": "some other video till thenbye take",
        "starttime": 736.6,
        "endtime": 742.76
    },
    {
        "text": "care",
        "starttime": 739.959,
        "endtime": 744.76
    },
    {
        "text": "brenet your",
        "starttime": 742.76,
        "endtime": 748.88
    },
    {
        "text": "golden I will",
        "starttime": 744.76,
        "endtime": 748.88
    }
]
def getytscript(video_id):
    try:
        # Try to fetch English transcript first
        fetched_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        print("English transcript not found. Trying auto-generated Hindi...")
        try:
            fetched_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        except NoTranscriptFound:
            print("No transcripts available for this video.")
            return None
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video.")
            return None
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

    # Convert to JSON format
    transcript_json = [
        {
            "text": snippet.get("text", ""),
            "starttime": snippet.get("start", 0),
            "endtime": snippet.get("start", 0) + snippet.get("duration", 0)
        }
        for snippet in fetched_transcript
    ]
    return json.dumps(transcript_json, indent=4, ensure_ascii=False)

def insertdb(video_id, url, transcript_json):
    existing = database_collection.find_one({"url": url})
    
    if existing:
        print(f"⚠️ Transcript for video_id '{video_id}' already exists. Skipping insert.")
        return False  # Optional: return False if not inserted

    # Insert if not present
    data = {
        "video_id": video_id,
        "url": url,
        "transcript": transcript_json
    }
    database_collection.insert_one(data)
    print("✅ Transcript saved to MongoDB successfully!")
    return True  # Optional: return True if inserted

@router.post("/get-transcript")
def get_transcript(data: VideoRequest):
    
    video_id = data.video_id

    # Fetch from MongoDB
    record = database_collection.find_one({"video_id": video_id}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Transcript not found in database")

    # Handle older JSON string format
    transcript = record.get("transcript", [])
    if isinstance(transcript, str):
        transcript = json.loads(transcript)

    record["transcript"] = transcript
    return JSONResponse(content=record)

@router.post("/get-transcript-by-time")
def get_transcript_by_time(data: TranscriptTimeRange):
    """
    POST /get-transcript-by-time
    {
        "video_id": "Ckc0gS9Kvrg",
        "start_time": 30,
        "end_time": 60
    }
    """
    # Fetch record from MongoDB
    record = database_collection.find_one({"video_id": data.video_id}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Transcript not found")

    transcript = record.get("transcript", [])

    # Convert if stored as string
    if isinstance(transcript, str):
        transcript = json.loads(transcript)

    # 🔍 Find entries that fall within the range
    filtered_transcript = [
        entry for entry in transcript
        if entry["endtime"] >= data.start_time and entry["starttime"] <= data.end_time
    ]

    if not filtered_transcript:
        return JSONResponse(content={"message": "No transcript found for given range."}, status_code=404)

    return {
        "video_id": data.video_id,
        "requested_start_time": data.start_time,
        "requested_end_time": data.end_time,
        "filtered_transcript": filtered_transcript,
        "total_entries": len(filtered_transcript)
    }
datatc={}
@router.post("/process_url")
def process_url(data: UrlData):
    received_url = data.url
    # print("URL from frontend:", received_url)
    ytid=get_youtube_id(received_url)
    print(ytid)
    tc=getytscript(ytid)
    insertdb(ytid,received_url,tc)
    print(tc)
    # get_transcript_by_time_range(ytid,0,30)
    return {"message": f"URL received successfully: {received_url}"}    

# @router.post("/ask-ai")
# async def ask_ai(request: ChatRequest):
#     """
#     Handles user questions about a YouTube video transcript.
#     """
#     try:
#         # # 2️⃣ Convert to Python list (if it’s JSON string)
#         transcript_data = getytscript(request.video_id)  # already a list/dict
#         print(transcript_data)
#         # # 3️⃣ Call your AI logic
#         output = main_ai.main(tc, user_question=request.question)
#         # print("ans",output.answer)
#         # 4️⃣ Return formatted result
#         # chat_doc = {
#         #     "video_id": request.video_id,
#         #     "question": request.question,
#         #     "answer": output,
#         #     "created_at": datetime.utcnow()
#         # }
#         # await database_collection.insert_one(chat_doc)
    
#         return {"answer": output}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask-ai")
async def ask_ai(request: ChatRequest):
    try:
        output = main_ai.main(tc, user_question=request.question)
        output = output.get("answer") if isinstance(output, dict) else str(output)
        # modules.tts_handler.getairesponce(output)
        chat_entry = {
            "question": request.question,
            "answer": output,
            "created_at": datetime.utcnow()
        }

        # ✅ Blocking synchronous call
        database_collection.update_one(
            {"video_id": request.video_id},
            {"$push": {"chats": chat_entry}},
            upsert=True
        )

        # 🕒 Small wait to ensure DB write completes
        time.sleep(0.5)

        return {"answer": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat-history/{video_id}")
async def get_last_chat_entry(video_id: str):
    """
    Returns the most recent question-answer pair for a given video ID.
    """
    try:
        doc = await database_collection.find_one(
            {"video_id": video_id},
            {"_id": 0, "chats": 1}
        )
        await asyncio.sleep(0.5)
        # print(doc)

        if not doc or not doc.get("chats"):
            raise HTTPException(status_code=404, detail="No chat history found for this video")

        last_chat = doc["chats"][-1]
        await asyncio.sleep(0.5)
        print(last_chat.get("answer"))

        print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ",last_chat["answer"])
        await modules.tts_handler.getairesponce(last_chat["answer"])  # ✅ await if async
        await asyncio.sleep(1)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching last chat: {str(e)}")