import React from 'react';
import { PRIMARY_COLOR } from '../utils/constants';

/** A reusable button component with the specified gradient and hover effect. */
const GradientButton = ({ children, onClick, className = '', disabled = false }) => (
    <button
        onClick={onClick}
        disabled={disabled}
        className={`
            ${className} px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform shadow-lg bg-linear-to-r from-${PRIMARY_COLOR}-500 to-fuchsia-600 hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed
    `}> {children} </button>
);

export default GradientButton;