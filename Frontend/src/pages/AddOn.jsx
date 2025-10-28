import React from 'react';
import { ClipboardList, FileText } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import GradientButton from '../components/GradientButton';

/** AddOn Page — Quiz & Summary Options */
const AddOn = ({ onGoBack, goToQuiz, goToSummary }) => {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-slate-900 text-white">
            <h2 className="text-3xl font-bold mb-10">Choose Your Next Step</h2>

            {/* Two balanced sections */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl w-full">
                {/* Quiz Section */}
                <div className="flex flex-col bg-slate-800/70 border border-slate-700 rounded-2xl p-8 shadow-xl hover:border-emerald-500/40 transition-all">
                    <FeatureCard
                        icon={ClipboardList}
                        title="Quick Quiz"
                        description="Test your understanding of the topic through short, text-based questions."
                    />
                    <div className="mt-6 text-slate-400 text-sm leading-relaxed">
                        <p>
                            The quiz consists of 5–10 short questions based on what you learned.
                            Type your answers freely — our AI checks your understanding contextually.
                        </p>
                    </div>
                    <div className="mt-auto flex justify-end pt-6">
                        <GradientButton onClick={goToQuiz}>Give Quiz</GradientButton>
                    </div>
                </div>

                {/* Summary Section */}
                <div className="flex flex-col bg-slate-800/70 border border-slate-700 rounded-2xl p-8 shadow-xl hover:border-indigo-500/40 transition-all">
                    <FeatureCard
                        icon={FileText}
                        title="Quick Summary"
                        description="Get a concise summary highlighting the key ideas and takeaways."
                    />
                    <div className="mt-6 text-slate-400 text-sm leading-relaxed">
                        <ul className="list-disc pl-5 space-y-1">
                            <li>Summarized main points</li>
                            <li>Important concepts simplified</li>
                            <li>Ready-to-revise format</li>
                        </ul>
                    </div>
                    <div className="mt-auto flex justify-end pt-6">
                        <GradientButton onClick={goToSummary}>Get Summary</GradientButton>
                    </div>
                </div>
            </div>

            {/* Go Back Button */}
            <div className="mt-10">
                <GradientButton onClick={onGoBack}>Go Back</GradientButton>
            </div>
        </div>
    );
};

export default AddOn;
