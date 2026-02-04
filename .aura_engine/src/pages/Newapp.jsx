import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Newapp() {
    const navigate = useNavigate();

    const el_1_ref = useRef(null);
    const el_2_ref = useRef(null);
    const el_3_ref = useRef(null);
    const el_4_ref = useRef(null);
    const el_5_ref = useRef(null);

    useEffect(() => {
        el_3_ref.current.style.color = 'black';
        el_5_ref.current.style.color = 'white';
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_1_ref}>Welcome to Aura! The New Ultimate Programming Language Built with determination by Kingenious Creative Studio</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_2_ref}>Building apps has never been easier like this!</p>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_3_ref} onClick={async () => {
        await new Promise(resolve => setTimeout(resolve, 3 * 1000));
        alert('Welcome to Aura! You are a pro now');
        window.location.reload();
        alert('Start Coding');
    }}>Get Started</button>
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_4_ref}>About Kingenious</h1>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_5_ref} onClick={() => {
        window.open('https://kcs-portfolio-seven.vercel.app/', '_blank');
    }}>About Me</button>
            </div>
        </div>
    );
}
