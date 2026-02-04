import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function Good() {
    const navigate = useNavigate();

    const el_1_ref = useRef(null);
    const el_2_ref = useRef(null);
    const el_3_ref = useRef(null);
    const el_4_ref = useRef(null);


    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <div className="p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300" ref={el_1_ref}>
            <h3 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">Good</h3>
            <p className="text-gray-600 dark:text-gray-400">Good is a card with a title and description</p>
        </div>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_2_ref} onClick={() => {
        window.open('https://x.com', '_blank');
    }}>Go back home</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_3_ref} onClick={() => {
        alert('I am good, thank you!');
    }}>how are you</button>
        <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200" ref={el_4_ref} onClick={() => {
        alert('Hello World');
    }}>show alert</button>
            </div>
        </div>
    );
}
