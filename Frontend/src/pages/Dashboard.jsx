import React, { useState } from 'react';
import { Link, Brain, Target, CheckCircle, Video } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import GradientButton from '../components/GradientButton';

/** Main Dashboard Page */
const Dashboard = ({ videoUrl, setVideoUrl, handleSubmitVideo }) => {
    const [mockLoading, setMockLoading] = useState(false);
    const [error, setError] = useState('');

    // ✅ YouTube link validation
    const isValidYouTubeUrl = (url) => {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w\-]{11}$/;
        return pattern.test(url.trim());
    };

    const onSubmit = () => {
        if (!isValidYouTubeUrl(videoUrl)) {
            setError('Please enter a valid YouTube video link!');
            return;
        }

        setError('');
        setMockLoading(true);
        setTimeout(() => {
            handleSubmitVideo();
            setMockLoading(false);
        }, 1500);
    };

    const featureData = [
        { icon: Brain, title: "Instant Explanations", description: "Get complex concepts broken down frame-by-frame." },
        { icon: Target, title: "Smart Context", description: "AI links video content to broader academic topics." },
        { icon: CheckCircle, title: "Personal Quizzes", description: "Test your understanding with automated questions." },
        { icon: Video, title: "Focus Mode", description: "Watch without distractions, keeping learning front and center." },
    ];

    return (
        <div className="flex flex-col min-h-screen p-4 md:p-10">
            <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-4 text-center">
                What do you want to learn today?
            </h2>
            <p className="text-xl text-slate-400 mb-10 text-center max-w-2xl mx-auto">
                Paste any educational YouTube link below to start your AI-guided learning session.
            </p>

            {/* Video URL Input */}
            <div className={`max-w-3xl mx-auto w-full mb-16 p-4 rounded-xl shadow-xl border border-slate-700 bg-slate-800/70 backdrop-blur-md`}>
                <div className="flex flex-col space-y-3">
                    <div className="flex space-x-3">
                        <div className="flex-1 relative">
                            <Link className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-indigo-400" />
                            <input
                                type="url"
                                placeholder="Paste your YouTube link here..."
                                value={videoUrl}
                                onChange={(e) => {
                                    setVideoUrl(e.target.value);
                                    if (error) setError('');
                                }}
                                className="w-full p-4 pl-12 rounded-xl border border-slate-600 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 bg-slate-800 text-slate-100"
                            />
                        </div>
                        <GradientButton onClick={onSubmit} disabled={!videoUrl || mockLoading}>
                            {mockLoading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Processing...
                                </span>
                            ) : (
                                'Start Learning'
                            )}
                        </GradientButton>
                    </div>

                    {/* ⚠️ Validation Error Message */}
                    {error && (
                        <p className="text-sm text-red-400 mt-1 text-left pl-1">{error}</p>
                    )}
                </div>
            </div>

            {/* Feature Highlights */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto w-full">
                {featureData.map((feature, index) => (
                    <FeatureCard key={index} {...feature} />
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
