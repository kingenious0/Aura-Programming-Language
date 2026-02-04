import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Testnl() {
    const navigate = useNavigate();

    const el_1_ref = useRef(null);
    const el_2_ref = useRef(null);
    const el_3_ref = useRef(null);
    const el_4_ref = useRef(null);
    const el_5_ref = useRef(null);
    const el_6_ref = useRef(null);
    const el_7_ref = useRef(null);
    const el_8_ref = useRef(null);
    const el_9_ref = useRef(null);
    const el_10_ref = useRef(null);
    const el_11_ref = useRef(null);
    const el_12_ref = useRef(null);
    const el_13_ref = useRef(null);
    const el_14_ref = useRef(null);
    const el_15_ref = useRef(null);

    useEffect(() => {
        el_3_ref.current.style.color = 'red';
        el_4_ref.current.style.transform = 'scale(1.2)';
        el_5_ref.current.style.display = 'none';
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_1_ref}>Natural Language Test</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_2_ref}>This is a test of the new natural language commands.</p>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_3_ref}>Red Button</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_4_ref}>Big Button</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_5_ref}>Hidden Button</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_6_ref} onClick={() => {
        el_6_ref.current.style.display = 'block';
    }}>Show Hidden</button>
        <input className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm" ref={el_7_ref} placeholder="Focus Test" />
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_8_ref} onClick={() => {
        
    }}>Focus It</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_9_ref} onClick={async () => {
        alert('Waiting...');
        await new Promise(resolve => setTimeout(resolve, 2 * 1000));
        alert('Done!');
    }}>Wait Test</button>
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_10_ref}>Old Text</h1>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_11_ref} onClick={() => {
        
    }}>Change Text</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_12_ref} onClick={() => {
        window.location.href = 'https://google.com';
    }}>Google</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_13_ref} onClick={() => {
        alert('Copied!');
    }}>Copy Me</button>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_14_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Fade Card</h3>
        </div>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_15_ref} onClick={() => {
        
    }}>Fade Out</button>
            </div>
        </div>
    );
}
