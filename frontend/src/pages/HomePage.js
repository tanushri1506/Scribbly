import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="content-box">
        <h1 className="title">🎨Scribbly</h1>
        <h2 className='slogan'>Scribble the Sky, Your Way</h2>
        <p className="subtitle">
          Turn Gestures into Art! <br />
          Create stunning sketches using hand gestures in real-time. <br />
          Choose your color, tweak the brush, and save your masterpiece.
        </p>
        <button className="start-btn" onClick={() => navigate('/draw')}>
          Start Drawing
        </button>
      </div>
    </div>
  );
}

export default HomePage;
