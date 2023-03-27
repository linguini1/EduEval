import React from "react";
import "./Results.css";

const courses = ["Course A", "Course B", "Course C", "Course D", "Course E"];
const positiveFeedback = "This is the positive feedback";
const negativeFeedback = "This is the negative feedback";

export default function Results(){
  return (
    <div className="container">
      <label htmlFor="course-select">Course Name:</label>
      <select id="course-select">
        {courses.map((course) => (
          <option key={course} value={course}>
            {course}
          </option>
        ))}
      </select>
      
      <div className="feedback-box pos">
          <textarea readonly value={positiveFeedback}></textarea>
      </div>
      <div className="feedback-box neg">
          <textarea readonly value={negativeFeedback}></textarea>
      </div>
    </div>
  );
};

