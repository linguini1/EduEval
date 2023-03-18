import React from "react";
import "./Results.css";

const courses = [
  "Course A",
  "Course B",
  "Course C",
  "Course D",
  "Course E",
];

const Results = () => {
  return (
    <div className="results-container">
      <h1>Results</h1>
      
      <div className="form-container">
        <label htmlFor="course-select">Course Name:</label>
        <select id="course-select">
          {courses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>

        <div className="feedback-forms">

          <div className="form-group">
            <label htmlFor="positive-feedback">Positive feedback:</label>
            <textarea id="positive-feedback"></textarea>
          </div>

          <div className="form-group">
            <label htmlFor="negative-feedback">Negative feedback:</label>
            <textarea id="negative-feedback"></textarea>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Results;