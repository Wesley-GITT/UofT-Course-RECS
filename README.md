# CSC111 Project 2 Report: UofT Course Recommendation System

This is a project written in python to recommend ARTSCI course to students.
Follow [this link](https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/project2/phase2/) to project requirement


## Tasks and Features

### Writing Report
    - Introduction (Who)
    - Description of Dataset (Who)
    - Computational overview (Who)  
    - Instructions for obtaining datasets and running your program (Who)
    - Changes to your project plan (Who)
    - Discussion (Who)
    - References Section (Who)
### Dataset (Wes)
  - Course
  - Reviews
### Features
  #### Recommendation:
  ##### Input
    - user input (courses completed, current courses, program, interest?)
    - load a graph (Wes)
  ##### Data Structure
  ###### Graph
    - Edges
      - scores on the review
    - Vertex:
      - review made by user
      - course
        - req (parent class)
          - init: use binary tree? load course req as boolean
          - prerequisite (children)
          - corequisite (children)
        - breadth requirement (int)
        - distribution requirement (int)
        - programme completion requirement (class)
  ##### Output
    - recommend (func; default-max: 3)

  #### Information Query
    - Input: course code/course name
    - Output: course information
