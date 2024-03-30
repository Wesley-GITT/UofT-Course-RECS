"""SCRAPE_COURSE
This is a python file that downloads all (latest) course information (of the Faculty of Art
and Science, St. George Campus ONLY) and convert it into csv files

The data for courses in 2023-2024 was generated from:
https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?page=1

The generated csv contains the following (10) columns, in the following order:

CODE: the code of the course (as displayed on acorn)
NAME: the name of the course (as displayed on acorn)
# PREV_CODE: code previously used for the course
# HOURS: hours of lectures, tutorials, labs, practicals
# DETAIL: further description of the course
PREREQ: prerequisite of the course
COREQ: corequisite of the course
# RECOMMENDED_PREP: recommended preparation for the course
# EXCLUSIONS: exlusive course
# DIST_REQ: distribution requirement (the old breath requirement)
BREADTH_REQ: breadth requirement, see here: https://artsci.calendar.utoronto.ca/hbahbsc-requirements

- Data with '#' at the beginning are ignored

NOTICE:
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from os.path import abspath
from bs4 import BeautifulSoup, Tag
from dataset_util import get_url_html, in_a_row, get_info_from_html


def get_course_info_from_html(block: Tag) -> dict[str, str]:
    """Helper function of scrape_course. Convert html to a mapping of course information."""
    css_selector_mapping = {
        "code_and_name": ".views-field-title",
        # "prev_code": "views-field-field-previous-course-number .field-content",
        # "hours": ".views-field-field-hours .field-content", "detail": ".views-field-body",
        "prereq": ".views-field-field-prerequisite .field-content",
        "coreq": ".views-field-field-corequisite .field-content",
        # "recommended_prep": ".views-field-field-recommended .field-content",
        # "exclusions": ".views-field-field-exclusion .field-content",
        # "dist_req": ".views-field-field-distribution-requirements .field-content",
        "breadth_req": ".views-field-field-breadth-requirements .field-content"
    }

    # Adjust some of the data
    course_data = get_info_from_html(block, css_selector_mapping)
    lst = course_data["code_and_name"].split(" - ")
    course_data["code"], course_data["name"] = lst.pop(0), str.join(" - ", lst)
    course_data.pop("code_and_name")
    return course_data


def scrape_course(save_dir: str = "", filename: str = "course.csv", lim: int = -1) -> None:
    """
    Scrape all the course information from the url specified.
    This method uses Beautiful Soup 4 to access DOM element in html.
    
    Preconditions:
      - lim >= 1
    """
    url = "https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?page=1"
    html_content = get_url_html(url)

    # Use Beautiful Soup to parse and access DOM element
    document = BeautifulSoup(html_content, 'html.parser')
    blocks = document.select(".no-break.w3-row.views-row")

    # Save the course information into csv
    save_path = abspath(f"{save_dir}/{filename}")
    num_record_saved = 0
    with open(save_path, "w") as w:
        for block in blocks:
            if num_record_saved >= lim and lim >= 1:
                break
            course_data = get_course_info_from_html(block)
            order = ["code", 'name', 'prereq', 'coreq', 'breadth_req']
            w.write(f"{in_a_row(course_data, order, '|')}\n")
            num_record_saved += 1


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1732'],
    #     'extra-imports': ['bs4', 'dataset_util', 'os.path'],
    #     'allowed-io': ['scrape_course'],
    #     'max-nested-blocks': 4
    # })

    scrape_course("dataset/", "course.csv")
