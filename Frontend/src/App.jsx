import React, { useState, useEffect, useCallback } from 'react';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import VideoChatPage from './pages/VideoChatPage';
import Header from './components/Header';
import AddOn from './pages/AddOn';
import QuizPage from './pages/Quiz';
import Summary from './pages/Summary';


/** Main App Component */
const App = () => {
    const [isAuthenticated, setAuthenticated] = useState(false);
    const [currentPage, setCurrentPage] = useState('dashboard'); 
    const [videoUrl, setVideoUrl] = useState('');

    // 🔹 Check authentication on load
    useEffect(() => {
        const token = localStorage.getItem('eduai_token');
        if (!token) {
            setCurrentPage('auth');
        } else {
            setAuthenticated(true);
            setCurrentPage('dashboard');
        }
    }, []);

    // 🔹 Update flow based on authentication
    useEffect(() => {
        if (isAuthenticated && currentPage === 'auth') {
            setCurrentPage('dashboard');
        } else if (!isAuthenticated) {
            setCurrentPage('auth');
        }
    }, [isAuthenticated, currentPage]);

    const handleSubmitVideo = useCallback(() => {
        if (videoUrl) setCurrentPage('video_chat');
    }, [videoUrl]);

    const handleLogout = useCallback(() => {
        setAuthenticated(false);
        setVideoUrl('');
        setCurrentPage('auth');
        localStorage.removeItem('eduai_token');
    }, []);

    const handleProfileClick = useCallback(() => {
        setCurrentPage('profile');
    }, []);

    const handleGoToDashboard = useCallback(() => {
        setCurrentPage('dashboard');
    }, []);

    /** 🔻 Renders active page */
    const renderContent = () => {
        switch (currentPage) {
            case 'auth':
                return <AuthPage setAuthenticated={setAuthenticated} />;

            case 'dashboard':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <Dashboard
                            videoUrl={videoUrl}
                            setVideoUrl={setVideoUrl}
                            handleSubmitVideo={handleSubmitVideo}
                        />
                    </>
                );

            case 'video_chat':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <VideoChatPage
                            videoUrl={videoUrl}
                            handleLogout={() => setCurrentPage('dashboard')}
                            handleNext={() => setCurrentPage('addon')}
                        />
                    </>
                );

            case 'addon':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <AddOn
                            onGoBack={() => setCurrentPage('video_chat')}
                            goToQuiz={() => setCurrentPage('quiz')}
                            goToSummary={() => setCurrentPage('summary')}
                        />
                    </>
                );

            case 'quiz':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <QuizPage onBackToAddOn={() => setCurrentPage('addon')} />
                    </>
                );

            case 'summary':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <Summary onBackToAddOn={() => setCurrentPage('addon')} />
                    </>
                );

            case 'profile':
                return (
                    <>
                        <Header handleLogout={handleLogout} />
                        <ProfilePage onGoToDashboard={handleGoToDashboard} />
                    </>
                );

            default:
                return <AuthPage setAuthenticated={setAuthenticated} />;
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 font-sans">
            <style>{`
                body {
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                }
                .custom-scrollbar::-webkit-scrollbar {
                    width: 8px;
                }
                .custom-scrollbar::-webkit-scrollbar-track {
                    background: #1e293b;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb {
                    background: #475569;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                    background: #64748b;
                }
            `}</style>
            {renderContent()}
        </div>
    );
};

export default App;
