import React from 'react';
import logo from '../media/logo2.png';
import './Navbar.css';

function Navbar() {
  return (
    <div >
      <nav>       
        <div className="navbar-items">
          <div className="logo">
            <a href="/"><img src={logo} /></a>
          </div>
          <a href="/feedback">Insert Feedback</a>
          <a  href="/results">Get Results</a>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;