import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Demofull() {
    const navigate = useNavigate();
    const [app_title, setAppTitle] = useState('Aura Demo');
    const [user_name, setUserName] = useState('John Doe');

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
    const el_16_ref = useRef(null);
    const el_17_ref = useRef(null);
    const el_18_ref = useRef(null);
    const el_19_ref = useRef(null);
    const el_20_ref = useRef(null);

    useEffect(() => {
        el_15_ref.current.classList.add('text-right');
        el_19_ref.current.classList.add('underline');
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <div className="" ref={el_1_ref} />
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_2_ref}>Welcome to Aura Programming Language</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_3_ref}>Build beautiful web applications using natural English commands!</p>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_4_ref} onClick={() => {
        alert('Hello from Aura!');
    }}>Say Hello</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_5_ref} onClick={() => {
        alert('This is an alert message!');
    }}>Show Alert</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_6_ref} onClick={() => {
        window.location.reload();
    }}>Refresh Page</button>
        <input className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm" ref={el_7_ref} placeholder="Enter your name" />
        <input className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm" ref={el_8_ref} placeholder="Enter your email" />
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_9_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Feature 1</h3>
            <p className="text-gray-600 dark:text-gray-400">Aura uses natural language syntax</p>
        </div>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_10_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Feature 2</h3>
            <p className="text-gray-600 dark:text-gray-400">Professional HTML output with modern design</p>
        </div>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_11_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Feature 3</h3>
            <p className="text-gray-600 dark:text-gray-400">Multiple themes: dark, light, and default</p>
        </div>
        <img className="rounded-xl shadow-lg max-w-full h-auto hover:scale-[1.02] transition-transform duration-300" ref={el_12_ref} src="https://via.placeholder.com/600x300" alt="Image" />
        <img className="rounded-xl shadow-lg max-w-full h-auto hover:scale-[1.02] transition-transform duration-300" ref={el_13_ref} src="https://via.placeholder.com/400x200" alt="Demo Image" />
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_14_ref} onClick={() => {
        alert('Form submitted successfully!');
    }}>Submit Form</button>
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_15_ref}>Contact Us</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_16_ref}>Fill out the form below to get in touch</p>
        <input className="w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm" ref={el_17_ref} placeholder="Your message" />
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_18_ref} onClick={() => {
        alert('Message sent! Thank you for contacting us.');
    }}>Send Message</button>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_19_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Waakye is nice</h3>
            <p className="text-gray-600 dark:text-gray-400">Waakye is a Ghanaian dish made from rice and beans cooked together. It is a popular breakfast dish in Ghana and is often served with a variety of side dishes.</p>
        </div>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_20_ref} onClick={() => {
        window.location.reload();
    }}>Show Waakye Card</button>
            </div>
        </div>
    );
}
