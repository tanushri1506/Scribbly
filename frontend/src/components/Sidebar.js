// frontend/src/Sidebar.js
import React from 'react';
import './Sidebar.css';
import { useNavigate } from "react-router-dom";

 
function Sidebar({ settings, setSettings, onClear, onUndo, onSave }) {

   const navigate = useNavigate();
 const handleEndSession = () => {
    fetch("http://localhost:5000/end_session", {
      method: "POST",
    }).then(() => {
      navigate("/", { replace: true });
    });
  };


  return (
    <div className="sidebar">
      <h3>Tools</h3>

      <label>Brush Size</label>
      <input
        type="range"
        min="1"
        max="20"
        value={settings.brushSize}
        onChange={(e) =>
          setSettings({ ...settings, brushSize: parseInt(e.target.value) })
        }
      />

      <label>Color</label>
      <select
        value={settings.color}
        onChange={(e) => setSettings({ ...settings, color: e.target.value })}
      >
        <option value="blue">Blue</option>
        <option value="green">Green</option>
        <option value="red">Red</option>
        <option value="yellow">Yellow</option>
      </select>

      <label>Shapes</label>
      <select
        value={settings.shape}
        onChange={(e) => setSettings({ ...settings, shape: e.target.value })}
      >
        <option value="free">Free</option>
        <option value="line">Line</option>
        <option value="rectangle">Rectangle</option>
        <option value="circle">Circle</option>
      </select>

      <button className="btn" onClick={onClear}>Clear</button>
      <button className="btn" onClick={onSave}>Save</button>


      <div className="end-session-wrapper">
          <button className="end-btn" onClick={handleEndSession}>
            End Session
          </button>
        </div>
    </div>
  );
}

export default Sidebar;
