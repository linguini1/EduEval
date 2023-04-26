import React, { useState, useEffect } from "react";
import { useFetch, api } from "../hooks/useFetch";
import "./Results.css";

export default function Results() {
  const [course_options, setCourseOptions] = useState(<option>Loading</option>);
  const [prof_options, setProfOptions] = useState(<option>Loading</option>);

  // Keep track of the select elements so we can access their values
  const prof_select = (
    <select id="prof-select" onChange={professorChange}>
      {prof_options}
    </select>
  );
  const course_select = (
    <select id="course-select" onChange={courseChange}>
      {course_options}
    </select>
  );

  // Fetch professors and courses
  const [index, index_loading] = useFetch(`${api}/index`);
  const [search_prof, setSearchProf] = useState(null);
  const [search_course, setSearchCourse] = useState(null);

  // Track feedback
  const [feedback, setFeedback] = useState({
    negative: "This is the negative feedback.",
    positive: "This is the positive feedback.",
  });

  useEffect(() => {
    fetch(`${api}/${search_prof}/${search_course}`)
      .then((response) => response.json())
      .then((response_data) => {
        setFeedback(response_data);
      });
  }, [search_prof, search_course]);

  // Create professor selection options everytime there is a new index
  useEffect(() => {
    if (!index_loading) {
      setProfOptions(
        Object.keys(index).map((prof) => (
          <option key={prof} value={prof}>
            {prof}
          </option>
        ))
      );
      setSearchProf(Object.keys(index)[0]); // First prof by default
    }
  }, [index_loading]);

  // Update the course selection options when there is a new index or when the prof selection has changed
  useEffect(() => {
    if (!index_loading && search_prof !== null) {
      setCourseOptions(
        index[search_prof].map((course) => (
          <option key={course} value={course}>
            {course}
          </option>
        ))
      );
    }
  }, [index_loading, search_prof]);

  // If any selection changes, we want to request the feedback
  function courseChange(e) {
    setSearchCourse(e.target.value);
  }

  // If the professor selection is change, re-request the course list based on the prof
  function professorChange(e) {
    setSearchProf(e.target.value);
    setSearchCourse(index[e.target.value][0]); // Make first course in list the new search course to avoid unwanted combos
  }

  return (
    <>
      <div className="selectors">
        <div className="select-box">
          <p>Professor:</p>
          {prof_select}
        </div>
        <div className="select-box">
          <p>Course:</p>
          {course_select}
        </div>
      </div>
      <div className="container">
        <div className="feedback-box pos">
          <label htmlFor="posLabel"> Positive Feedback</label>
          <textarea id="posLabel" readonly value={feedback.positive}></textarea>
        </div>
        <div className="feedback-box neg">
          <label htmlFor="negLabel">Negative Feedback</label>
          <textarea id="negLabel" readonly value={feedback.negative}></textarea>
        </div>
      </div>
    </>
  );
}
