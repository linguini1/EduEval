import React from 'react';
import logo from '../media/logo2.png';
import './Navbar.css';

export default function Navbar({ children }) {
  return (
    <nav>
      <div className="nav-items">
        <div className="logo">
          <img src={logo} alt="Logo" />
        </div>
        <div className="nav-links">{children}</div>
      </div>
    </nav>
  );
}