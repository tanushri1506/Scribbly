// src/components/Footer.js
import React from 'react';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <p>Built with ❤️ using React, Flask & MediaPipe</p>
      <div className="footer-links">
        <a href="https://github.com/tanushri1506" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>
        <a href="mailto:barsainyatanushri555@gmail.com">Contact</a>
        <a href="https://tanushri1506.github.io/Portfolio/" target="_blank" rel="noopener noreferrer">
          Portfolio
        </a>
      </div>
      <p className="footer-copy">&copy; {new Date().getFullYear()} Air Sketch. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
