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
import requests


def get_url_html(url: str) -> str:
    """Get html content of a webpage at specified url."""
    r = requests.get(url, allow_redirects=True)
    return r.content


def in_a_row(mapping: dict[str, str], order: list) -> str:
    """
    Helper function of html_to_csv. Return course information in a row of csv string.
    
    Precondition:
      - all(key in mapping for key in order)
    """
    block_str = ""
    for key in order:
        block_str += mapping[key] + ":"

    return block_str[:len(block_str) - 1]


def get_text_from_html_element(block: Tag, css_selector: str) -> str:
    """
    Helper function of course_block_reader. Extract text from an html element.
    If the element is not found, return an empty string.
    """
    elements = block.select(css_selector)
    if len(elements) == 0:
        return ""
    else:
        return elements[0].get_text().strip().replace("\n", "")


def get_course_info_from_html(block: Tag) -> dict[str, str]:
    """Helper function of html_to_csv. Convert html to a mapping of course information."""
    css_selector_mapping = {
        "code_and_name": ".views-field-title",
        # "prev_code": "views-field-field-previous-course-number .field-content",
        # "hours": ".views-field-field-hours .field-content", "detail": ".views-field-body",
        "prereq": ".views-field-field-prerequisite .field-content",
        "coreq": ".views-field-field-corequisite .field-content",
        # "recommended_prep": ".views-field-field-recommended .field-content",
        # "exclusions": ".views-field-field-exclusion .field-content",
        # "dist_req": ".views-field-field-distribution-requirements .field-content",
        "breadth_req": ".views-label-field-breadth-requirements .field-content"
    }

    course_data = {}
    for key in css_selector_mapping:
        course_data[key] = get_text_from_html_element(block, css_selector_mapping[key])

    # Adjust some of the data
    lst = course_data["code_and_name"].split(" - ")
    course_data["code"], course_data["name"] = lst.pop(0), str.join(" - ", lst)
    course_data.pop("code_and_name")
    return course_data


def scrape_course(url: str, save_dir: str = "") -> None:
    """
    Scrape all the course information from the url specified.
    When entry_per_file is set to -1, data will not be stored in multiple files
    This method uses Beautiful Soup 4 to access DOM element in html.
    """
    html_content = get_url_html(url)

    # Use Beautiful Soup to parse and access DOM element
    document = BeautifulSoup(html_content)
    blocks = document.select(".no-break.w3-row.views-row")

    # Save the course information into csv
    save_path = abspath(f"{save_dir}/course.csv")
    with open(save_path, "w") as w:
        for block in blocks:
            course_data = get_course_info_from_html(block)
            order = ["code", 'name', 'prereq', 'coreq', 'breadth_req']
            w.write(f"{in_a_row(course_data, order)}\n")


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1732'],
    #     'extra-imports': ['bs4', 'requests', 'os.path'],
    #     'allowed-io': ['scrape_course'],
    #     'max-nested-blocks': 4
    # })

    course_info_url = "https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?page=1"
    scrape_course(course_info_url, "dataset/")
