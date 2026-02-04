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
    const el_21_ref = useRef(null);
    const el_22_ref = useRef(null);
    const el_23_ref = useRef(null);
    const el_24_ref = useRef(null);
    const el_25_ref = useRef(null);

    useEffect(() => {
        el_15_ref.current.classList.add('text-right');
        el_19_ref.current.classList.add('italic');
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
        <img className="rounded-xl shadow-lg max-w-full h-auto hover:scale-[1.02] transition-transform duration-300" ref={el_12_ref} src="data:image/webp;base64,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" alt="Image" />
        <img className="rounded-xl shadow-lg max-w-full h-auto hover:scale-[1.02] transition-transform duration-300" ref={el_13_ref} src="data:image/webp;base64,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" alt="Demo Image" />
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
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_21_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Kofi is going to church</h3>
            <p className="text-gray-600 dark:text-gray-400">Kofi is going to church on sunday</p>
        </div>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_22_ref} onClick={() => {
        window.location.reload();
    }}>show kofi card</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_23_ref} onClick={() => {
        alert('testing ai features');
    }}>testing ai features</button>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_24_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">going to school today</h3>
            <p className="text-gray-600 dark:text-gray-400">going to school today</p>
        </div>
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_25_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">i am here</h3>
            <p className="text-gray-600 dark:text-gray-400">i am here</p>
        </div>
            </div>
        </div>
    );
}
