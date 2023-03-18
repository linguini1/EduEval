import React from "react";
import "./Feedback.css";

const courses = ["Course A", "Course B", "Course C", "Course D", "Course E"];

const Feedback = () => {
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

      <div className="button-container">
        <button className="submitButton" type="submit">
          Submit
        </button>
      </div>
    </div>
  );
};

export default Feedback;