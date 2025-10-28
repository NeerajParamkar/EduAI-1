import React, { useState, useMemo } from 'react';
import { LogIn, UserPlus } from 'lucide-react';
import InputField from '../components/InputField';
import GradientButton from '../components/GradientButton';
import { BACKGROUND_COLOR, CARD_BG, PRIMARY_COLOR } from '../utils/constants';

/** Landing and Authentication Page */
const AuthPage = ({ setAuthenticated }) => {
    const [currentTab, setCurrentTab] = useState('login'); // 'login' or 'signup'
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleAuth = () => {
        // Mock Auth Logic
        console.log(`${currentTab} attempt for ${email}`);
        // In a real app, this would be an API call.
        // We simulate successful authentication.
        setAuthenticated(true);
    };

    const isSignup = currentTab === 'signup';
    const isFormValid = useMemo(() => {
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
                        onClick={() => setCurrentTab('login')}
                        className={`flex-1 py-2 text-center rounded-lg font-medium transition-all duration-300 ${currentTab === 'login' ? `bg-${PRIMARY_COLOR}-600 text-white shadow-xl` : 'text-slate-400 hover:text-white'}`}>
                        <LogIn className="inline w-5 h-5 mr-2" /> Login
                    </button>
                    <button
                        onClick={() => setCurrentTab('signup')}
                        className={`flex-1 py-2 text-center rounded-lg font-medium transition-all duration-300 ${currentTab === 'signup' ? `bg-${PRIMARY_COLOR}-600 text-white shadow-xl` : 'text-slate-400 hover:text-white'}`}
                    >
                        <UserPlus className="inline w-5 h-5 mr-2" /> Sign Up
                    </button>
                </div>

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

                <GradientButton onClick={handleAuth} disabled={!isFormValid} className="w-full mt-8">
                    {isSignup ? 'Create Account' : 'Continue to Learning'}
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

export default AuthPage;