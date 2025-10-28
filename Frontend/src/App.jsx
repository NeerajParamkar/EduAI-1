import React, { useState, useEffect, useCallback } from 'react';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import VideoChatPage from './pages/VideoChatPage';
import Header from './components/Header';

/** Main App Component */
const App = () => {
    const [isAuthenticated, setAuthenticated] = useState(false);
    const [currentPage, setCurrentPage] = useState('dashboard'); // 'auth', 'dashboard', 'video_chat', 'profile'
    const [videoUrl, setVideoUrl] = useState('');

    // Initial setup: check authentication status
    useEffect(() => {
        const token = localStorage.getItem('eduai_token');
        if (!token) {
            setCurrentPage('auth');
        } else {
            setAuthenticated(true);
            setCurrentPage('dashboard');
        }
    }, []);

    // Update flow based on authentication
    useEffect(() => {
        if (isAuthenticated && currentPage === 'auth') {
            setCurrentPage('dashboard');
        } else if (!isAuthenticated) {
            setCurrentPage('auth');
        }
    }, [isAuthenticated, currentPage]);

    const handleSubmitVideo = useCallback(() => {
        if (videoUrl) {
            setCurrentPage('video_chat');
        }
    }, [videoUrl]);

    const handleLogout = useCallback(() => {
        setAuthenticated(false);
        setVideoUrl('');
        setCurrentPage('auth');
        localStorage.removeItem('eduai_token');
    }, []);

    /** 🔗 Handles Profile Button Click */
    const handleProfileClick = useCallback(() => {
        setCurrentPage('profile');
    }, []);

    /** 🧠 Handles "Go to Dashboard" click inside Profile */
    const handleGoToDashboard = useCallback(() => {
        setCurrentPage('dashboard');
    }, []);

    /** Page rendering */
    const renderContent = () => {
        switch (currentPage) {
            case 'auth':
                return <AuthPage setAuthenticated={setAuthenticated} />;

            case 'dashboard':
                return (
                    <>
                        <Header
                            handleLogout={handleLogout}
                            onProfileClick={handleProfileClick}
                        />
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
                        <Header
                            handleLogout={handleLogout}
                            onProfileClick={handleProfileClick}
                        />
                        <VideoChatPage
                            videoUrl={videoUrl}
                            handleLogout={() => setCurrentPage('dashboard')}
                        />
                    </>
                );

            case 'profile':
                return (
                    <>
                        <Header
                            handleLogout={handleLogout}
                            onProfileClick={handleProfileClick}
                        />
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
