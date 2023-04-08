import "./App.css";
import React from "react";

//Pages
import Feedback from "./pages/Feedback";
import Results from "./pages/Results";

//Components
import {Routes, Route} from "react-router-dom"
import PageLink from "./components/PageLink";
import Navbar from "./components/Navbar";


function App() {
  return (
    <div id="App">
      <Navbar>
        <PageLink to="/">Feedback</PageLink>
        <PageLink to="/results">Results</PageLink>
      </Navbar>
      <Routes>
        <Route path="/" element={<Feedback />}></Route>
        <Route path="/results" element={<Results />}></Route>
      </Routes>
    </div>
    
  );
}

export default App;