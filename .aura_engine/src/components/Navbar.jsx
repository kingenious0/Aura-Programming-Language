import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Aura
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              
              <Link to="/" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${location.pathname === '/' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}`}>
                Home
              </Link>
            
              <Link to="/demo" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${location.pathname === '/demo' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}`}>
                Demo
              </Link>
            
              <Link to="/about" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${location.pathname === '/about' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}`}>
                About
              </Link>
            
              <Link to="/example" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${location.pathname === '/example' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}`}>
                Example
              </Link>
            
              <Link to="/good" className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${location.pathname === '/good' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}`}>
                Good
              </Link>
            
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-200 hover:text-blue-500 focus:outline-none">
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white dark:bg-gray-900 shadow-lg">
            
              <Link to="/" onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                Home
              </Link>
            
              <Link to="/demo" onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                Demo
              </Link>
            
              <Link to="/about" onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                About
              </Link>
            
              <Link to="/example" onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                Example
              </Link>
            
              <Link to="/good" onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                Good
              </Link>
            
          </div>
        </div>
      )}
    </nav>
  );
}
