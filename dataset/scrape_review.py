"""SCRAPE_REVIEW
This is a python file that downloads all (latest) course review (of the Faculty of Art
and Science, St. George Campus ONLY) and convert it into csv files

The data for reviews in 2023-2024 was generated from course evaluation page from quercus:


The generated csv contains the following (10) columns, in the following order:

DEPT: department which offers the course
DIV: faculty which offers the course
CODE: course code as displayed on ACORN
LEC: lecture code as displayed on ACORN
LNAME: last name of the professor teaching the lecture
FNAME: first name of the professor teaching the lecture
TERM: term (fall/winter/summer) in which the course is offered
YEAR: year in which the course is offered
ITEM1: I found the course intellectually stimulating.
ITEM2: The course provided me with a deeper understanding of the subject matter.
ITEM3: The instructor created a course atmosphere that was conducive to my learning.
ITEM4: Course projects, assignments, tests and/or exams improved my understanding of the course material.
ITEM5: Course projects, assignments, tests and/or exams provided opportunity for me to demonstrate an understanding of the course material.
ITEM6: Overall, the quality of my learning experience in this course was:
ITEM9: The instructor generated enthusiasm for learning in the course.
ITEM10: Compared to other courses, the workload for this course was…
ITEM11: I would recommend this course to other students.
STNUM: number of students invited to complete the evaluation
STRSP: number of students completed the evaluation

- Data with '#' at the beginning are ignored

NOTICE:
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def go_to_evaluation_page(utorid: str, passwd: str) -> webdriver:
    """
    Navigate browser to quercus page and then evaluation page
    """

    
    


def scrape_review(utorid: str, passwd: str, save_dir: str = "") -> None:
    """
    Scrape reviews of courses in recent years and save it into a csv file
    Require utorid and password to open the page.
    """

