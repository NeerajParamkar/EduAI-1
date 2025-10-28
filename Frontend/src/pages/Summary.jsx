import React from 'react';
import GradientButton from '../components/GradientButton';

const Summary = ({ onBackToAddOn }) => {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 p-6 text-white">
            {/* Title */}
            <h2 className="text-3xl font-bold mb-6 text-indigo-400">
                Summary 📘
            </h2>

            {/* Summary Box */}
            <div className="bg-slate-800/70 backdrop-blur-md border border-slate-700 rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
                <p className="text-lg text-slate-300 leading-relaxed mb-8">
                    {/* Placeholder for generated summary */}
                    <span className="italic text-slate-400">
                        Summary content will appear here...
                    </span>
                </p>

                <div className="flex justify-center">
                    <GradientButton onClick={onBackToAddOn}>
                        Back to Add-On
                    </GradientButton>
                </div>
            </div>
        </div>
    );
};

export default Summary;
