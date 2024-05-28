# CSC111 Project 2 Report: UofT Course Recommendation System

This is a project written in python to recommend ARTSCI course to students.
Follow [this link](https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/project2/phase2/) to project requirement

## Getting Started

### Install Chrome:
Download and install Google Chrome at https://www.google.com/chrome/

If you have already installed chrome, please make sure your browser version is no less than 123.0.0000.00

### Install Chromedriver
Download and chromedriver 124.0.000.00 from https://googlechromelabs.github.io/chrome-for-testing/#stable. Your should download the one with chromedriver at the first column.

If you are using Linux-Arm, you can also download chromedriver from https://github.com/electron/electron/releases/tag/v30.0.1.

Place your chromedriver at an appropriate location

Your python version should be not less than 3.10

### Install below python packages using pip
- python-ta~=2.7.0
- selenium==4.9.0
- requests==2.31.0
- beautifulsoup4==4.12.3

To start selenium correctly, specify the location of webdriver in the python code.
```Python
  from selenium import webdriver
  driver = webdriver.Chrome(executable_path='ABSOLUTE_PATH\TO\CHROMEDRIVER')    
```

Then you should be able to scrape the data and run the course recommendation program.

## Tasks and Features

### Writing Report
- Introduction
- Description of Dataset
- Computational overview
- Instructions for obtaining datasets and running your program
- Changes to your project plan
- Discussion
- References Section
### Dataset
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
  - professor
  - breadth requirement
  - programme
  - course
  - course-level
##### Output
- recommend (func; default-max: 3 for each course)
