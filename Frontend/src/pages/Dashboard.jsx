import React, { useState } from 'react';
import { Link, Brain, Target, CheckCircle, Video } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import GradientButton from '../components/GradientButton';
import { CARD_BG, TEXT_COLOR, PRIMARY_COLOR } from '../utils/constants';
import { processYoutubeUrl } from '../utils/api';

/** Main Dashboard Page (After Login) */
const Dashboard = ({ videoUrl, setVideoUrl, handleSubmitVideo }) => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const onSubmit = async () => {
        // Validate URL
        if (!videoUrl || !videoUrl.trim()) {
            setError('Please enter a YouTube URL');
            return;
        }

        // Basic YouTube URL validation
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
        if (!youtubeRegex.test(videoUrl)) {
            setError('Please enter a valid YouTube URL');
            return;
        }

        setLoading(true);
        setError('');
        setSuccess('');

        try {
            // Send URL to backend
            const response = await processYoutubeUrl(videoUrl);
            
            console.log('Backend response:', response);
            setSuccess('Video processed successfully!');
            
            // Navigate to video chat page after successful processing
            setTimeout(() => {
                handleSubmitVideo();
            }, 1000);
            
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
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
            <div className={`max-w-3xl mx-auto w-full mb-8 p-4 rounded-xl shadow-xl border border-slate-700 ${CARD_BG}`}>
                {/* Error Message */}
                {error && (
                    <div className="mb-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
                        {error}
                    </div>
                )}

                {/* Success Message */}
                {success && (
                    <div className="mb-4 p-3 bg-green-500/10 border border-green-500/50 rounded-lg text-green-400 text-sm">
                        {success}
                    </div>
                )}

                <div className="flex space-x-3">
                    <div className="flex-1 relative">
                        <Link className={`absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-${PRIMARY_COLOR}-400`} />
                        <input
                            type="url"
                            placeholder="Paste your YouTube link here... (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
                            value={videoUrl}
                            onChange={(e) => {
                                setVideoUrl(e.target.value);
                                setError('');
                                setSuccess('');
                            }}
                            onKeyPress={(e) => {
                                if (e.key === 'Enter' && !loading) {
                                    onSubmit();
                                }
                            }}
                            disabled={loading}
                            className={`w-full p-4 pl-12 rounded-xl border border-slate-600 focus:ring-2 focus:ring-${PRIMARY_COLOR}-500 focus:border-${PRIMARY_COLOR}-500 outline-none transition duration-200 bg-slate-800 ${TEXT_COLOR} disabled:opacity-50 disabled:cursor-not-allowed`}
                        />
                    </div>
                    <GradientButton onClick={onSubmit} disabled={!videoUrl || loading}>
                        {loading ? (
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