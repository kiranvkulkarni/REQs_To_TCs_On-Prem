import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="p-4 text-center text-sm text-gray-500 dark:text-gray-400">
      © {new Date().getFullYear()} Camera TestGen — On-Prem BDD Test Case Generator
    </footer>
  );
};

export default Footer;