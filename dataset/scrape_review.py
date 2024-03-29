"""SCRAPE_REVIEW
This is a python file that downloads all (latest) course review (of the Faculty of Art
and Science, St. George Campus ONLY) and convert it into csv files

The data for reviews in 2023-2024 was generated from course evaluation page from Quercus Page:

The generated csv contains the following (?) columns, in the following order, 

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
ITEM5: Course projects, assignments, tests and/or exams provided opportunity for me to demonstrate an understanding
       of the course material.
ITEM6: Overall, the quality of my learning experience in this course was, 
ITEM9: The instructor generated enthusiasm for learning in the course.
ITEM10: Compared to other courses, the workload for this course was…
ITEM11: I would recommend this course to other students.
STNUM: number of students invited to complete the evaluation
STRSP: number of students completed the evaluation

- Data with '#' at the beginning are ignored

NOTICE, 
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from os.path import abspath
from getpass import getpass
from multiprocessing import Process, Manager
from time import sleep
from bs4 import BeautifulSoup, Tag
from util import in_a_row, get_info_from_html
from review_page import EvalPage


def get_review_info_from_html(block: Tag) -> dict[str, str]:
    """Helper function of scrape_review. Convert html to a mapping of course information."""
    css_selector_list = [
        "dept", "div", "code_lec", "lname", "fname", "term", "year", "item1", "item2",
        "item3", "item4", "item5", "item6", "item9", "item10", "item11", "stnum", "strsp"
    ]
    css_selector_mapping = {}
    for i in range(len(css_selector_list)):
        item = css_selector_list[i]
        css_selector_mapping[item] = f"td:nth-child({i + 1})"

    review_data = get_info_from_html(block, css_selector_mapping)
    # Adjust some of the data
    code_lec = review_data["code_lec"]
    code = block.get("sk")
    tmp = code_lec[::-1]
    if "-" in tmp:
        tmp = tmp[:tmp.index("-")]
    else:
        tmp = tmp[:7]
    lec = tmp[::-1].strip()
    review_data["code"] = code
    review_data["lec"] = lec
    review_data.pop("code_lec")
    return review_data


def print_progress(i: int, total: int, length: int = 50) -> None:
    """Print the progress bar"""
    bar_str = int(i / total * float(length)) * "#" + int((total - i) / total * float(length)) * "-"
    percent = round(i / total * 100, 1)
    print(f"[{bar_str}] {percent}% | {i} out of {total}", end="\r")


def progress_monitor(dct: dict[int, str], total: int, length: int = 50) -> None:
    """Print the overall progress constantly untill done."""
    completed = len(dct)
    print_progress(completed, total, length)
    sleep(1)

    if completed < total:
        progress_monitor(dct, total, length)


def open_and_save(utorid: str, passwd: str, index: int, process_num: int, row_data: dict[int, str]) -> None:
    """
    Open a single process of webdriver to save data of each pages from start to end inclusive
    into the row_data list and return the list to user.
    This method uses Beautiful Soup 4 to access DOM element in html.
    """
    page = EvalPage(utorid, passwd, 100)

    inlen = page.get_num_pages() // process_num
    if page.get_num_pages() % process_num != 0:
        inlen += 1

    start = inlen * index
    end = min(inlen * (index + 1), page.get_num_records() - 1)

    for i in range(start + 1, end + 1):
        html = page.get_data(i)
        document = BeautifulSoup(html, "html.parser")
        blocks = document.select(".gData")
        for j in range(len(blocks)):
            order = [
                "dept", "div", "code", "lec", "lname", "fname", "term", "year", "item1", "item2",
                "item3", "item4", "item5", "item6", "item9", "item10", "item11", "stnum", "strsp"
            ]
            row_data[(i - 1) * 100 + j] = in_a_row(get_review_info_from_html(blocks[j]), order)


def scrape_review(save_dir: str = "") -> None:
    """
    Scrape all the review information from the url specified.
    """

    print("Authentication Required.\n")
    utorid = input("Enter your UTORid: ")
    passwd = getpass("Enter your password: ")
    print()

    process_num = 1
    processes = []
    with Manager() as manager:
        row_data = manager.dict()

        monitor = Process(target=progress_monitor, args=(row_data, 38632))
        monitor.start()

        for i in range(process_num):
            p = Process(target=open_and_save, args=(utorid, passwd, i, process_num, row_data,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        monitor.join()

        save_path = f"{save_dir}/review.csv"
        with open(abspath(save_path), "w") as w:
            sorted_data = sorted(row_data.items())
            for _, value in sorted_data:
                w.write(f"{value}\n")


if __name__ == "__main__":
    scrape_review("dataset/")

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['bs4', 'util', 'os.path', 'time', 'multiprocessing', 'review_page', 'getpass'],
    #     'allowed-io': ['scrape_review'],
    #     'max-nested-blocks': 4
    # })
