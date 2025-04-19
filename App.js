import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import WhatIsPCB from './pages/WhatIsPCB';
import Tips from './pages/Tips';
import Viewer from './pages/Viewer';
import Calculator from './pages/Calculator';
import PCBDiagram from './pages/PCBdiagram'; // Import PCB Diagram page
import './App.css';

function App() {
  return (
    <Router>
      <div className="navbar">
        <div className="navbar-left">
          <div className="logo">MaternoCare</div>
          <nav>
             <Link to="/">Home</Link>
             <Link to="/whatispcb">What is PCB?</Link>
             <Link to="/tips">Tips for Women</Link>
             <Link to="/pcbdrawing">PCB Diagram</Link>
             <Link to="/viewer">View PCB Compounds</Link>
             <Link to="/calculator">Risk Calculator</Link>
          </nav>
        </div>
      </div>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/whatispcb" element={<WhatIsPCB />} />
        <Route path="/tips" element={<Tips />} />
        <Route path="/viewer" element={<Viewer />} />
        <Route path="/calculator" element={<Calculator />} />
        <Route path="/pcbdrawing" element={<PCBDiagram />} /> {/* Route for PCB Diagram */}
      </Routes>
    </Router>
  );
}

export default App;
