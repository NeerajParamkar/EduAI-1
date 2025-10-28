import React, { useState, useRef, useEffect } from "react";
import { Brain, LogOut } from "lucide-react";

/** Header Component (Used on Dashboard and Video/Chat pages) */
const Header = ({ handleLogout }) => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    // Close dropdown if clicked outside
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <header className="sticky top-0 z-10 w-full p-4 border-b border-slate-700/50 bg-slate-800/70 backdrop-blur-md shadow-xl">
            <div className="flex justify-between items-center max-w-7xl mx-auto">
                {/* Logo */}
                <div className="text-2xl font-bold tracking-tight text-white flex items-center">
                    <Brain className="w-7 h-7 mr-2 text-indigo-400" />
                    Edu<span className="text-indigo-400">AI</span>
                </div>

                {/* Profile Dropdown (Logout only) */}
                <div className="relative" ref={dropdownRef}>
                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className="flex items-center space-x-2 p-2 rounded-full border border-slate-700 bg-slate-700 hover:bg-slate-600 transition duration-200 text-slate-200"
                    >
                        <div className="w-9 h-9 rounded-full bg-emerald-500 flex items-center justify-center text-white font-bold">
                            U
                        </div>
                    </button>

                    {isOpen && (
                        <div className="absolute right-0 mt-2 w-36 bg-slate-800 border border-slate-700 rounded-xl shadow-xl overflow-hidden">
                            <button
                                onClick={() => {
                                    setIsOpen(false);
                                    handleLogout();
                                }}
                                className="flex items-center w-full px-4 py-2 text-sm text-red-400 hover:bg-red-600/20 transition"
                            >
                                <LogOut className="w-4 h-4 mr-2" />
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;
