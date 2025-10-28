import React, { useState, useRef, useEffect } from 'react';
import { Bot, MessageSquare, Send } from 'lucide-react';

/** AI Chatbox Component */
const ChatBox = ({ videoUrl }) => {
    const getEmbedId = (url) => {
        try {
            const urlObj = new URL(url);
            if (urlObj.hostname.includes('youtube.com')) {
                return urlObj.searchParams.get('v');
            } else if (urlObj.hostname.includes('youtu.be')) {
                return urlObj.pathname.substring(1);
            }
        } catch (e) {
            console.error("Invalid URL for embedding:", e);
        }
        return 'LXb3fo5XOSo';
    };

    const embedId = getEmbedId(videoUrl) || 'LXb3fo5XOSo';

    const [messages, setMessages] = useState([
        { id: 1, role: 'ai', text: `Hello! I'm your AI Tutor. I've analyzed the video content. Ask me anything about ${embedId ? 'this video' : 'the solar system'}!` },
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [isThinking, setIsThinking] = useState(false);

    const handleSendMessage = () => {
        if (inputMessage.trim() === '' || isThinking) return;

        const newMessage = { id: Date.now(), role: 'user', text: inputMessage.trim() };
        setMessages((prev) => [...prev, newMessage]);
        setInputMessage('');
        setIsThinking(true);

        // Mock AI Response
        setTimeout(() => {
            const mockResponse = {
                id: Date.now() + 1,
                role: 'ai',
                text: `That's an excellent question based on the segment around 1:45! The core principle discussed there is the **${newMessage.text.length % 2 === 0 ? 'principle of quantum entanglement' : 'law of diminishing returns'}**, which the speaker uses to explain the concept of resource allocation. Would you like a more detailed summary of that section `,
            };
            setMessages((prev) => [...prev, mockResponse]);
            setIsThinking(false);
        }, 2500);
    };

    const messageEndRef = useRef(null);
    useEffect(() => {
        messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div className={`lg:col-span-1 flex flex-col bg-slate-800/70 backdrop-blur-md p-4 rounded-2xl shadow-xl border border-slate-700 h-[80vh] overflow-y-auto`}>

            <div className="flex items-center justify-between border-b border-slate-700 pb-3 mb-3">
                <h3 className="text-xl font-bold text-white flex items-center">
                    <Bot className={`w-6 h-6 mr-2 text-emerald-400`} /> Ask Your AI Tutor
                </h3>
                <MessageSquare className="w-5 h-5 text-slate-400" />
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] p-3 rounded-xl shadow-md transition-all duration-300 ${msg.role === 'user' ? `bg-indigo-600 text-white rounded-br-none` : 'bg-slate-700 text-slate-200 rounded-tl-none'}`}>
                            <p className="text-sm"> {msg.text} </p>
                        </div>
                    </div>
                ))}
                {isThinking && (
                    <div className="flex justify-start">
                        <div className="bg-slate-700 text-slate-200 p-3 rounded-xl rounded-tl-none">
                            <span className="text-sm italic animate-pulse">AI is thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messageEndRef} /> </div>

            {/* Chat Input */}
            <div className="mt-4 flex items-center">
                <input
                    type="text"
                    placeholder="Type your question..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') handleSendMessage();
                    }}
                    disabled={isThinking}
                    className={`flex-1 p-3 rounded-l-xl bg-slate-800 border border-slate-700 focus:ring-1 focus:ring-indigo-500 outline-none text-slate-100`} />
                <button
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim() || isThinking}
                    className={` p-3 rounded-r-xl transition-all duration-200 bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-50 disabled:cursor-not-allowed `}
                    title="Send Message">
                    <Send className="w-5 h-5" />
                </button>
            </div>
        </div>
    );
};

export default ChatBox;