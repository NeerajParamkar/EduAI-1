import React from 'react';
import { CARD_BG, TEXT_COLOR, PRIMARY_COLOR } from '../utils/constants';

/** Input component. */
const InputField = ({ label, type = 'text', placeholder, value, onChange, icon: Icon }) => (
    <div className="flex flex-col space-y-2">
        <label className="text-sm font-medium text-slate-300">{label}</label>
        <div className="relative">
            {Icon && <Icon className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-${PRIMARY_COLOR}-400`} />}
            <input
                type={type}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                className={` w-full p-3 pl-10 ${Icon ? 'pl-10' : 'pl-4'} ${CARD_BG} border border-slate-700 rounded-xl focus:ring-2 focus:ring-${PRIMARY_COLOR}-500 focus:border-${PRIMARY_COLOR}-500 outline-none transition duration-200 ${TEXT_COLOR}`}/>
        </div>
    </div>
);

export default InputField;