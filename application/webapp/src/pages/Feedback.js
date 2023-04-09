import React, {useState, useEffect} from "react";

import "./Feedback.css";

const courses = ["Course A", "Course B", "Course C", "Course D", "Course E"];

export default function Feedback() {

  const [file, setFile] = useState(null);

  const handleFileUpload = (event) => {
    // Checks if uploaded file is correct type
    if (event.target.files[0].type !== 'text/csv'){
        console.log('Invalid file type. Please select a CSV file.');
        return ;
    }
    setFile(event.target.files[0]); 
  }


  async function handleSubmit (event) {

    if (file != null){
      event.preventDefault(); // Cancels the default action of the event
      const formData = new FormData(); //Creates FormData to easily send file as part of HTTP request
      formData.append('file', file);

      //Send the file to the server
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      })

        .then((response) => {
          console.log('File uploaded successfully!');
        })
        .catch((error) => {
          console.error('Error uploading file:', error);
        });
    }    
  };


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
        <input type="file" id="upload-file" name="upload-file" onChange={handleFileUpload} accept= ".csv"/>
      </div>

      <div className="button-container">
        <button className="submitButton" type="submit" onClick = {handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
};

