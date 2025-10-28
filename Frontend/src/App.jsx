import React, { useState, useEffect, useCallback } from 'react';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import VideoChatPage from './pages/VideoChatPage';
import Header from './components/Header';
import { BACKGROUND_COLOR } from './utils/constants';

/** Main App Component */
const App = () => {
    const [isAuthenticated, setAuthenticated] = useState(false);
    const [currentPage, setCurrentPage] = useState('dashboard'); // 'auth', 'dashboard', 'video_chat'
    const [videoUrl, setVideoUrl] = useState('');

    // Initial setup: check authentication status
    useEffect(() => {
        // In a real app, this would check a token/session
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
        // Mock logout action
        setAuthenticated(false);
        setVideoUrl('');
        setCurrentPage('auth');
    }, []);

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
                        />
                    </>
                );
            default:
                return <AuthPage setAuthenticated={setAuthenticated} />;
        }
    };

    return (
        <div className={`min-h-screen ${BACKGROUND_COLOR} font-sans`}>
            {/* Custom Scrollbar Styling */}
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
                }`}</style>
            {renderContent()}
        </div>
    );
};

export default App;