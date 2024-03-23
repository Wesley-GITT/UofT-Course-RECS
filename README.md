# CSC111 Project 2 Report: UofT Course Recommendation System

This is a project written in python to recommend ARTSCI course to students.
Follow [this link](https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/project2/phase2/) to project requirement


## Data structure

This project mainly uses graph to recommend courses in uoft

## Task Assignment

- Writing Report
    - Introduction (Who)
    - Description of Dataset (Who)
    - Computational overview (Who)
    - Instructions for obtaining datasets and running your program (Who)
    - Changes to your project plan (Who)
    - Discussion (Who)
    - References Section (Who)
- Dataset (Wes)
- Features
    - Recommendation:
      - Input (?)
      - Data Structure
        - Graph
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
        - load a graph (func) (?)
        - recommend (func; default-max: 3)
      - Output
        - Courses

    - Information Query
      - Input: course code/course name

## Features

There is a list of features we tend to accomplish for this project. Here is a guide to follow:
- Add a line for each of a new feature.
- Add a sublist identifying how to achieve the feature (be specific, e.g. what object should be created and what are the instant attributes and methods).
- Add a sublist identifying hot to test this feature.
- Below is two examples of one of the feature of the RECS.

### Dataset

- Course (code)
- Reviews (code)


### A list of Features

- Recommendation:
  - Input:
    - Take students current programme as input
    - Optional: previous courses
    - Optional: year the student is in
  - Data Structure
    - Graph
      - Edges
        - scores on the review
      - Vertex:
        - review made by user
        - course
          - prerequisite (class)
            - TODO
          - corequisite (class)
            - TODO
          - breadth requirement
          - distribution requirement
          - programme completion requirement
    - load a graph (func)
    - recommend (func; default-max: 3)
  - Output
    - Courses

- Information Query
  - Input: course code/course name
