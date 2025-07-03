import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DrawingPage from './pages/DrawingPage';
import './App.css';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <>
            <HomePage />
            <Footer/>
          </>  
        } />
        <Route path="/draw" element={<DrawingPage />} />
      </Routes>
    </Router>
  );
}

export default App;
