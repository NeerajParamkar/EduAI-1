import React, { useState } from 'react';
import GradientButton from '../components/GradientButton';

const QuizPage = ({ onBackToAddOn }) => {
    const [userAnswer, setUserAnswer] = useState('');

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 p-6 text-white">
            {/* Heading */}
            <h2 className="text-3xl font-bold mb-6 text-indigo-400">
                Quiz Time 🧠
            </h2>

            {/* Question Card */}
            <div className="bg-slate-800/70 backdrop-blur-md border border-slate-700 rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
                <p className="text-lg mb-6 text-slate-200">
                    {/* Placeholder for question text */}
                    <span className="italic text-slate-400">Question will appear here...</span>
                </p>

                {/* Answer Input */}
                <input
                    type="text"
                    placeholder="Type your answer here..."
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    className="w-full p-4 rounded-xl border border-slate-600 bg-slate-900 text-slate-100 focus:ring-2 focus:ring-indigo-500 outline-none transition mb-6"
                />

                {/* Buttons */}
                <div className="flex justify-between">
                    <GradientButton onClick={onBackToAddOn}>Back</GradientButton>
                    <GradientButton>Submit Answer</GradientButton>
                </div>
            </div>
        </div>
    );
};

export default QuizPage;
