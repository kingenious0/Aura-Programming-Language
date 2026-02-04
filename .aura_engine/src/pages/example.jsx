import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Example() {
    const navigate = useNavigate();
    const [user_name, setUserName] = useState('Akwasi');
    const [app_title, setAppTitle] = useState('Welcome to Aura By Kingenious Creative Studio');

    const el_1_ref = useRef(null);
    const el_2_ref = useRef(null);
    const el_3_ref = useRef(null);
    const el_4_ref = useRef(null);
    const el_5_ref = useRef(null);
    const el_6_ref = useRef(null);

    useEffect(() => {
        el_1_ref.current.classList.add('text-center');
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_1_ref}>Welcome to Aura Programming Language</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_2_ref}>This is a revolutionary way to code using natural English!</p>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_3_ref} onClick={() => {
        alert('Hello from Aura! 🎉');
    }}>Click Me Here</button>
        <input className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm" ref={el_4_ref} placeholder="Enter your name" />
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_5_ref} onClick={() => {
        alert('Form submitted successfully!');
    }}>Submit Form</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_6_ref} onClick={() => {
        navigate('/about');
    }}>About Me</button>
            </div>
        </div>
    );
}
