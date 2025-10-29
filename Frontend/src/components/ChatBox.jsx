import React, { useState, useRef, useEffect } from "react";
import { Bot, MessageSquare, Send } from "lucide-react";
import { CARD_BG, TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR } from "../utils/constants";

/** 💡 AI Chatbox Component — connects with FastAPI backend */
const ChatBox = ({ videoUrl }) => {
  // Extract YouTube video ID from URL
  const getEmbedId = (url) => {
    try {
      const urlObj = new URL(url);
      if (urlObj.hostname.includes("youtube.com")) {
        return urlObj.searchParams.get("v");
      } else if (urlObj.hostname.includes("youtu.be")) {
        return urlObj.pathname.substring(1);
      }
    } catch (e) {
      console.error("Invalid video URL:", e);
    }
    return "LXb3fo5XOSo"; // default fallback
  };

  const embedId = getEmbedId(videoUrl) || "LXb3fo5XOSo";

  // Chat state
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "ai",
      text: `👋 Hello! I'm your AI Tutor. I've analyzed this YouTube video. Ask me anything about its content!`,
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isThinking, setIsThinking] = useState(false);
const handleFetchHistory = async () => {
  try {
    const res = await fetch(`http://localhost:8000/transcript/chat-history/${embedId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    

    // Since backend returns a single object, not an array:

    // setMessages((prev) => [...prev, aiMsg]);
  } catch (err) {
    console.error("❌ Error fetching history:", err);
  }
};


  // 🧠 Handle sending a message
const handleSendMessage = async () => {
  if (!inputMessage.trim() || isThinking) return;

  const userMsg = { id: Date.now(), role: "user", text: inputMessage.trim() };
  setMessages((prev) => [...prev, userMsg]);
  setInputMessage("");
  setIsThinking(true);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5 * 60 * 1000); // 5 min timeout

  try {
    const res = await fetch("http://localhost:8000/transcript/ask-ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_id: embedId,
        question: userMsg.text,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);

    const data = await res.json();
    console.log("🧠 Full AI Response:", data.answer.answer);

    // ✅ Safely extract only the readable text
    let answerText = "";
    if (typeof data.answer === "string") {
      answerText = data.answer;
    } else if (data.answer && typeof data.answer === "object") {
      // if backend sends an object, extract its text property or stringify
      answerText = data.answer.text || JSON.stringify(data.answer, null, 2);
    } else {
      answerText = "🤖 Sorry, I couldn’t generate a response.";
    }

    const aiMsg = {
      id: Date.now() + 1,
      role: "ai",
      text: answerText,
    };

    setMessages((prev) => [...prev, aiMsg]);
  } catch (err) {
    console.error("❌ Backend error:", err);
    let errorText = "⚠️ Error: Unable to connect to AI backend.";
    if (err.name === "AbortError") {
      errorText = "⏳ Timeout: AI took too long to respond (5 minutes limit).";
    }
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + 2,
        role: "ai",
        text: errorText,
      },
    ]);
  } finally {
    setIsThinking(false);
  }
};



  // 🔁 Auto-scroll to bottom on new messages
  const messageEndRef = useRef(null);
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🧱 UI
  return (
    <div
      className={`lg:col-span-1 flex flex-col h-[60vh] lg:h-auto ${CARD_BG} p-4 rounded-2xl shadow-xl border border-slate-700`}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-700 pb-3 mb-3 flex">
        <h3 className="text-xl font-bold text-white flex items-center">
          <Bot className={`w-6 h-6 mr-2 text-${SECONDARY_COLOR}-400`} />
          Ask Your AI Tutor
        </h3>
        <MessageSquare className="w-5 h-5 text-slate-400" />
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
  {messages.map((msg) => {
    let displayText = msg.text;

    try {
      // Try parsing if it's a JSON string like '{ "answer": "..." }'
      const parsed = JSON.parse(msg.text);
      if (parsed && parsed.answer) {
        displayText = parsed.answer;
      }
    } catch {
      // Not JSON, display as is
      displayText = msg.text;
    }

    return (
      <div
        key={msg.id}
        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
      >
        <div
          className={`max-w-[80%] p-3 rounded-xl shadow-md transition-all duration-300 ${
            msg.role === "user"
              ? "bg-indigo-600 text-white rounded-br-none"
              : "bg-slate-700 text-slate-200 rounded-tl-none"
          }`}
        >
          <p className="text-sm whitespace-pre-line">{displayText}</p>
          {msg.role !== "user" && (
          <button
            onClick={handleFetchHistory}
            className="mt-2 px-3 py-1 bg-slate-600 text-white text-xs rounded-lg hover:bg-slate-500"
          >
            speak
          </button>
        )}
        </div>
      </div>
    );
  })}

  {/* Thinking Animation */}
  {isThinking && (
    <div className="flex justify-start">
      <div className="bg-slate-700 text-slate-200 p-3 rounded-xl rounded-tl-none">
        <span className="text-sm italic animate-pulse">🤔 AI is thinking...</span>
      </div>
    </div>
  )}
</div>


      {/* Input Section */}
      <div className="mt-4 flex items-center">
        <input
          type="text"
          placeholder="Type your question..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
          disabled={isThinking}
          className={`flex-1 p-3 rounded-l-xl bg-slate-800 border border-slate-700 focus:ring-1 focus:ring-${PRIMARY_COLOR}-500 outline-none ${TEXT_COLOR}`}
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputMessage.trim() || isThinking}
          className={`p-3 rounded-r-xl transition-all duration-200 bg-${PRIMARY_COLOR}-600 hover:bg-${PRIMARY_COLOR}-500 text-white disabled:opacity-50 disabled:cursor-not-allowed`}
          title="Send Message"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
