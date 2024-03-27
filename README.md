# CSC111 Project 2 Report: UofT Course Recommendation System

This is a project written in python to recommend course to students.
Follow [this link](https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/project2/phase2/) to project requirement


## Tasks and Features

### Writing Report
- Introduction
- Description of Dataset
- Computational overview
- Instructions for obtaining datasets and running your program
- Changes to your project plan
- Discussion
- References Section
### Dataset (Wes)
- Course
- Reviews
### Features
#### Recommendation:
##### Input
- user input (courses completed, courses passed (optional), programme interested in?)
- load a graph
##### Data Structure
###### Graph
- Edges
  - scores on the review
- Vertex:
  - review made by user
  - breadth requirement
  - programme
  - course
    - prerequisite
    - corequisite
##### Output
- recommend (func; default-max: 3 for each course)

#### Information Query
- Input: course code/course name
- Output: course information
