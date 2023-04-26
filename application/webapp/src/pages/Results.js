import React, { useEffect } from "react";
import { useFetch, api } from "../hooks/useFetch";
import "./Results.css";

const positiveFeedback = "This is the positive feedback";
const negativeFeedback = "This is the negative feedback";

export default function Results() {
  // Fetch professors and courses
  const [professors, profs_loading] = useFetch(`${api}/profs`);
  const [courses, courses_loading] = useFetch(`${api}/courses`);

  let course_options = [<option>Loading</option>];

  let prof_options;
  if (!profs_loading) {
    prof_options = professors.map((prof) => (
      <option key={prof} value={prof}>
        {prof}
      </option>
    ));
  } else {
    prof_options = [<option>Loading</option>];
  }

  useEffect(() => {
    console.log(courses);
    if (!courses_loading) {
      course_options = courses.map((course) => (
        <option key={course} value={course}>
          {course}
        </option>
      ));
    }
  }, [courses_loading]);

  return (
    <div className="container">
      <label htmlFor="course-select" name="course">
        Course Name:
      </label>
      <select id="course-select">{course_options}</select>
      <div className="feedback-box pos">
        <label htmlFor="posLabel"> Positive Feedback</label>
        <textarea id="posLabel" readonly value={positiveFeedback}></textarea>
      </div>
      <div className="feedback-box neg">
        <label htmlFor="negLabel"> Negative Feedback</label>
        <textarea id="negLabel" readonly value={negativeFeedback}></textarea>
      </div>
    </div>
  );
}
