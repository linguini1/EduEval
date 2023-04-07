import React from "react";
import "./Feedback.css";

const courses = ["Course A", "Course B", "Course C", "Course D", "Course E"];

export default function Feedback() {
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    // do something with the uploaded file
  }

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

      <div >
        <label htmlFor="upload-file" className="upload-file">Upload Review File:</label> 
        <input type="file" id="upload-file" name="upload-file" onChange={handleFileUpload}/>
      </div>

      <div className="button-container">
        <button className="submitButton" type="submit">
          Submit
        </button>
      </div>
    </div>
  );
};

