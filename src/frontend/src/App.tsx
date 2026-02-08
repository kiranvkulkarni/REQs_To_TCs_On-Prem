import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Review from './pages/Review';
import Export from './pages/Export';
import FeedbackLog from './pages/FeedbackLog';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

const App: React.FC = () => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  return (
    <Router>
      <div className={`min-h-screen transition-colors duration-200 ${theme === 'dark' ? 'bg-gray-900 text-white' :
'bg-gray-50 text-gray-900'}`}>
        <Navbar theme={theme} setTheme={setTheme} />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/review/:id" element={<Review />} />
            <Route path="/export" element={<Export />} />
            <Route path="/feedback" element={<FeedbackLog />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;