import React from 'react';
import { Brain } from 'lucide-react';
import { CARD_BG, PRIMARY_COLOR } from '../utils/constants';

/** Header Component (Used on Dashboard and Video/Chat) */
const Header = ({ handleLogout }) => (
    <header className={`sticky top-0 z-10 w-full p-4 border-b border-slate-700/50 ${CARD_BG} shadow-xl`}>
        <div className="flex justify-between items-center max-w-7xl mx-auto">
            <div className={`text-2xl font-bold tracking-tight text-white flex items-center`}>
                <Brain className={`w-7 h-7 mr-2 text-${PRIMARY_COLOR}-400`} />
                Edu<span className={`text-${PRIMARY_COLOR}-400`}>AI</span>
            </div>
            <div className="relative">
                <button
                    onClick={handleLogout}
                    className={`
                        flex items-center space-x-2 p-2 rounded-full border border-slate-700 bg-slate-700 hover:bg-slate-600 transition duration-200 text-slate-200 text-sm font-medium
                        `}> 
                    <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-white font-bold">
                        U
                    </div>
                    <span>Logout</span>
                </button>
            </div>
        </div>
    </header>
);

export default Header;