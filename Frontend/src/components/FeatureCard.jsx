import React from 'react';
import { CARD_BG, SECONDARY_COLOR } from '../utils/constants';

/** A feature card for the dashboard highlights. */
const FeatureCard = ({ icon: Icon, title, description }) => (
    <div
        className={`
            ${CARD_BG} p-6 rounded-2xl border border-slate-700/50 shadow-xl flex flex-col items-center text-center transform transition-all duration-300 hover:shadow-2xl hover:border-${SECONDARY_COLOR}-500/50 hover:bg-slate-700/80`}>
        <Icon className={`w-10 h-10 text-${SECONDARY_COLOR}-400 mb-4`} />
        <h3 className="text-lg font-semibold mb-2 text-white">{title}</h3>
        <p className="text-slate-400 text-sm">{description}</p>
    </div>
);

export default FeatureCard;