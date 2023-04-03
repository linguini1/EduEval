# Data Collection System

## Usage
Add queries to the `query.json` file so they can be scraped from [RateMyProf](). The format of a query is as follows:

```JSON
{
  "school": "School Name",
  "professors": [
    "Professor One",
    "Professor Two",
    ...
  ]
}
```
The professors in each query must be the full names of the professors that attend the school for that query. Multiple
queries can be added for different schools.

Once run, the program will display which school, professor and course it is currently recording ratings for in the 
following way:
```text
SchoolName: Professor One - COURSE2001
School Name: Professor One - COURSE2002
School Name: Professor Two - COURSE1004
...
```

Once the queries are completed, they will be written to a CSV file in this format:
```csv
school,professor,course,comment
School Name,Professor One,COURSE2001,"This prof is great! Loved this course, 10/10 would recommend."
School Name,Professor One,COURSE2002,"Hated this class honestly. Prof is great but take this course in the summer."
School Name,Professor Two,COURSE1004,"Professor Two is so down to earth! They speak too quietly though."
```
