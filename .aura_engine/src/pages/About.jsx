import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, Link } from 'react-router-dom';

export default function About() {
    const navigate = useNavigate();

    const el_1_ref = useRef(null);
    const el_2_ref = useRef(null);

    useEffect(() => {
        el_2_ref.current.classList.add('text-center');
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm" ref={el_1_ref}>About Kingenious Creative Studio</h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl" ref={el_2_ref}>Kingenious Creative Studio is a web development company that specializes in building high-quality websites for small businesses and organizations. We are a team of experienced developers who are passionate about creating beautiful and functional websites that help our clients achieve their goals.</p>
            </div>
        </div>
    );
}
