"""SCRAPE_REVIEW
This is a python file that downloads all (latest) course review (of the Faculty of Art
and Science, St. George Campus ONLY) and convert it into csv files

The data for reviews in 2023-2024 was generated from course evaluation page on Quercus:

The generated csv contains the following (19) columns, in the following order, 

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
from dataset_util import in_a_row, get_info_from_html
from review_page import EvalPage, QuercusPage


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


def print_progress(i: int, total: int, length: int = 50, prefix: str = "") -> None:
    """Print the progress bar"""
    bar_str = int(i / total * float(length)) * "#" + int((total - i) / total * float(length)) * "-"
    percent = round(i / total * 100, 1)
    print(f"{prefix} [{bar_str}] {percent}% | {i} out of {total}", end="\r")


def progress_monitor(dct: dict[int, str], total: int, length: int = 50, prefix: str = "") -> None:
    """Print the overall progress constantly untill done."""
    completed = len(dct)

    while completed < total:
        completed = len(dct)
        print_progress(completed, total, length, prefix)
        sleep(0.01)


def open_and_save(url: str, index: int, process_num: int, row_data: dict[int, str], lim: int = -1, max_records: int = 10) -> None:
    """
    Open a single process of webdriver to save data of each pages from start to end inclusive
    into the row_data list and return the list to user.
    This method uses Beautiful Soup 4 to access DOM element in html.

    Preconditions:
      - lim >= 1
      - max_records in [5, 10, 15, 20, 25, 50, 100]
    """
    page = EvalPage(url, max_records)

    total_r = page.get_num_records()
    if lim >= 1:
        total_r = lim
    total_p = total_r // max_records
    if total_r % max_records != 0:
        total_p += 1
    inlen = total_p // process_num
    if total_r % process_num != 0:
        inlen += 1

    start = inlen * index + 1
    end = min(inlen * (index + 1) + 1, total_p + 1)

    for i in range(start, end):
        html = page.get_data(i)
        document = BeautifulSoup(html, "html.parser")
        blocks = document.select(".gData")
        for j in range(len(blocks)):
            record_index = (i - 1) * max_records + j
            if record_index >= total_r:
                return

            order = [
                "dept", "div", "code", "lec", "lname", "fname", "term", "year", "item1", "item2",
                "item3", "item4", "item5", "item6", "item9", "item10", "item11", "stnum", "strsp"
            ]
            row_data[record_index] = in_a_row(get_review_info_from_html(blocks[j]), order)


def scrape_review(save_dir: str = "", filename: str = "review.csv", lim: int = -1, max_records: int = 10, process_num: int = 1) -> None:
    """
    Scrape all the review information from the url specified.
    lim: number of dataset to download. Set to -1 to download all data
    max_records: number of data to download each time
    process_num: number of webdrivers to download at the same time

    Note:
      - A relationship between the maximum number of process, the total number of data and number of data to download each time is:
        maximum number of process * number of data to download each time < total number of data.
      - The number of process shouldn't be greater than some number, depending on the memory of your machine.

    Example:
      - For 20 data, run this:
        scrape_review("<directory>", "<filename>", 20, process_num = 2)

      - For all the data, run this:
        scrape_review("<directory>", "<filename>", -1, process_num = 64)

    Preconditions:
      - lim >= 1
      - process_num >= 1
      - max_records in [5, 10, 15, 20, 25, 50, 100]
    """

    print("Authentication Required.\n")
    utorid = input("Enter your UTORid: ")
    passwd = getpass("Enter your password: ")
    print("\nLoading Quercus and Evaluation Page...", end="\r")
    url = QuercusPage().get_link(utorid, passwd)

    processes = []
    with Manager() as manager:
        row_data = manager.dict()

        total_r = min(lim, 38632)

        max_process_num = total_r // max_records
        if total_r % max_records != 0:
            max_process_num += 1

        if process_num > max_process_num:
            print("Warning: too many processes are used. The number of process is adjusted")
            process_num = max_process_num

        for i in range(process_num):
            p = Process(target=open_and_save, args=(url, i, process_num, row_data, lim, max_records,))
            p.start()
            processes.append(p)

        sleep(10)
        print("Loading Quercus and Evaluation Page...Done")
        monitor = Process(target=progress_monitor, args=(row_data, total_r, 50, "Downloading data:",))
        monitor.start()

        for p in processes:
            p.join()

        monitor.join()
        print("Downloading data...Done ")
        print("Saving data to csv file...", end="\r")

        save_path = f"{save_dir}/{filename}"
        with open(abspath(save_path), "w") as w:
            sorted_data = sorted(row_data.items())
            for _, value in sorted_data:
                w.write(f"{value}\n")

        print("Saving data to csv file...Done\n")


if __name__ == "__main__":
    # scrape_review("dataset/", "review_large.csv", lim=1600, max_records=100, process_num=12)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['bs4', 'dataset_util', 'os.path', 'time', 'multiprocessing', 'review_page', 'getpass'],
        'allowed-io': ['scrape_review'],
        'max-nested-blocks': 4
    })
