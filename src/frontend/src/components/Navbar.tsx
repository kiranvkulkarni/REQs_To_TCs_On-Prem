import React from 'react';
import { Link } from 'react-router-dom';

interface NavbarProps {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

const Navbar: React.FC<NavbarProps> = ({ theme, setTheme }) => {
  return (
    <nav className={`p-4 shadow-md ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'}`}>
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">📸 Camera TestGen</Link>
        <div className="flex space-x-4">
          <Link to="/" className="hover:underline">Dashboard</Link>
          <Link to="/export" className="hover:underline">Export</Link>
          <Link to="/feedback" className="hover:underline">Feedback</Link>
          <button
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
            className="px-3 py-1 rounded bg-gray-200 dark:bg-gray-700"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;