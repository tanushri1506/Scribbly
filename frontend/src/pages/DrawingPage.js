import React, { useState, useEffect } from "react";
import "./DrawingPage.css";
import Sidebar from "../components/Sidebar";

function DrawingPage() {
  const [settings, setSettings] = useState({
    brushSize: 5,
    color: "blue",
    shape:'free'
  });
  
  const [canvasUrl, setCanvasUrl] = useState("");
  const API_BASE = "http://localhost:5000";
  

  useEffect(() => {
    fetch(`${API_BASE}/set_tools`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(settings),
    });
  }, [settings]);

  useEffect(() => {
    fetch("http://localhost:5000/session_status")
      .then((res) => res.json())
      .then((data) => {
        if (!data.active) {
          window.location.replace("/");
        }
      });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCanvasUrl(`http://localhost:5000/canvas_feed?${Date.now()}`);
    }, 100);
    return () => clearInterval(interval);
  }, []);

  const handleClear = () => {
    fetch(`${API_BASE}/clear`, { method: "POST" });
  };

  const handleSave = () => {
    fetch(`${API_BASE}/save`, {
      method: "POST",
    })
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "air_sketch.png";
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      });
  };

 
  return (
    <div className="App">
      <Sidebar
        settings={settings}
        setSettings={setSettings}
        onClear={handleClear}
        onSave={handleSave}
      />

      <div className="main-content">
        <div className="content-area">
          <div className="panel video-panel">
            <h2 className="panel-title">Live Drawing</h2>
            <div className="media-box">
              <img
                src="http://localhost:5000/video_feed"
                alt="Live Sketch Stream"
                className="media"
              />
            </div>
          </div>

          <div className="panel canvas-panel">
            <h2 className="panel-title">Canvas Preview</h2>
            <div className="media-box">
              {canvasUrl ? (
                <img src={canvasUrl} alt="Canvas Preview" className="media" />
              ) : (
                <div className="media placeholder">Canvas not ready</div>
              )}
            </div>
          </div>
        </div>

        
      </div>
    </div>
  );
}

export default DrawingPage;
