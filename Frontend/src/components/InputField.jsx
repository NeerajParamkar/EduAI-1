import React from 'react';

/** Input component. */
const InputField = ({ label, icon: Icon, ...props }) => (
    <div className="flex flex-col space-y-2">
        <label className="text-sm font-medium text-slate-300">{label}</label>
        <div className="relative">
            {Icon && <Icon className={`absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-indigo-400`} />}
            <input
                {...props}
                className={` w-full p-3 pl-10 ${Icon ? 'pl-10' : 'pl-4'} bg-slate-800/70 backdrop-blur-md border border-slate-700 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 text-slate-100`}/>
        </div>
    </div>
);

export default InputField;