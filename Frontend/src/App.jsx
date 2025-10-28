import React, { useState, useEffect, useCallback } from 'react';
import { LogIn, UserPlus } from 'lucide-react';
import InputField from './components/InputField';
import GradientButton from './components/GradientButton';
import Dashboard from './pages/Dashboard';
import VideoChatPage from './pages/VideoChatPage';
import Header from './components/Header';
import { BACKGROUND_COLOR, CARD_BG, PRIMARY_COLOR } from './utils/constants';
import { signup, login } from './utils/api';

/** Auth Page Component */
const AuthPage = ({ setAuthenticated }) => {
    const [currentTab, setCurrentTab] = useState('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAuth = async () => {
        setLoading(true);
        setError('');
        
        try {
            let response;
            if (currentTab === 'signup') {
                response = await signup(email, password, confirmPassword);
            } else {
                response = await login(email, password);
            }
            
            // Store the access token
            if (response.access_token) {
                localStorage.setItem('authToken', response.access_token);
                localStorage.setItem('eduai_token', response.access_token); // For compatibility
            }
            
            // Store user email
            localStorage.setItem('userEmail', email);
            
            setAuthenticated(true);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const isSignup = currentTab === 'signup';
    const isFormValid = React.useMemo(() => {
        if (isSignup) {
            return email && password && confirmPassword && password === confirmPassword && password.length >= 6;
        }
        return email && password;
    }, [email, password, confirmPassword, isSignup]);

    return (
        <div className={`flex items-center justify-center min-h-screen ${BACKGROUND_COLOR} p-4`}>
            <div className={`w-full max-w-md p-8 sm:p-10 rounded-3xl border border-slate-700 shadow-2xl ${CARD_BG}`}>
                <h1 className="text-3xl font-extrabold text-white text-center mb-6">EduAI</h1>
                <p className="text-center text-slate-400 mb-8 text-lg">Learn Smarter with AI-Powered Explanations.</p>

                {/* Tab Switcher */}
                <div className={`flex ${CARD_BG.split('/')[0]} p-2 rounded-xl mb-8 border border-slate-700`}>
                    <button
                        onClick={() => {
                            setCurrentTab('login');
                            setError('');
                        }}
                        className={`flex-1 py-2 text-center rounded-lg font-medium transition-all duration-300 ${currentTab === 'login' ? `bg-${PRIMARY_COLOR}-600 text-white shadow-xl` : 'text-slate-400 hover:text-white'}`}>
                        <LogIn className="inline w-5 h-5 mr-2" /> Login
                    </button>
                    <button
                        onClick={() => {
                            setCurrentTab('signup');
                            setError('');
                        }}
                        className={`flex-1 py-2 text-center rounded-lg font-medium transition-all duration-300 ${currentTab === 'signup' ? `bg-${PRIMARY_COLOR}-600 text-white shadow-xl` : 'text-slate-400 hover:text-white'}`}
                    >
                        <UserPlus className="inline w-5 h-5 mr-2" /> Sign Up
                    </button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mb-6 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
                        {error}
                    </div>
                )}

                <div className="space-y-6">
                    <InputField
                        label="Email Address"
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        icon={LogIn}
                    />
                    <InputField
                        label="Password"
                        type="password"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        icon={LogIn}
                    />
                    {isSignup && (
                        <InputField
                            label="Confirm Password"
                            type="password"
                            placeholder="••••••••"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            icon={LogIn}
                        />
                    )}
                </div>

                <GradientButton 
                    onClick={handleAuth} 
                    disabled={!isFormValid || loading} 
                    className="w-full mt-8"
                >
                    {loading ? 'Please wait...' : (isSignup ? 'Create Account' : 'Continue to Learning')}
                </GradientButton>

                <div className="text-center mt-4">
                    <a href="#" className={`text-sm text-${PRIMARY_COLOR}-400 hover:text-${PRIMARY_COLOR}-300 transition-colors`}>
                        {isSignup ? 'Already have an account? Login' : 'Forgot password?'}
                    </a>
                </div>
            </div>
        </div>
    );
};

/** Main App Component */
const App = () => {
    const [isAuthenticated, setAuthenticated] = useState(false);
    const [currentPage, setCurrentPage] = useState('auth'); // 'auth', 'dashboard', 'video_chat'
    const [videoUrl, setVideoUrl] = useState('');
    const [loading, setLoading] = useState(true);

    // Initial setup: check authentication status
    useEffect(() => {
        const token = localStorage.getItem('authToken') || localStorage.getItem('eduai_token');
        if (token) {
            setAuthenticated(true);
            setCurrentPage('dashboard');
        } else {
            setCurrentPage('auth');
        }
        setLoading(false);
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
        // Clear all auth tokens
        localStorage.removeItem('authToken');
        localStorage.removeItem('eduai_token');
        localStorage.removeItem('userEmail');
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

    // Show loading state while checking authentication
    if (loading) {
        return (
            <div className={`flex items-center justify-center min-h-screen ${BACKGROUND_COLOR}`}>
                <div className="text-white text-xl">Loading...</div>
            </div>
        );
    }

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
                }
            `}</style>
            {renderContent()}
        </div>
    );
};

export default App;