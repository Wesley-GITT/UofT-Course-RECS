"""SCRAPE_COURSE
This is a python file that downloads all (latest) course information (of the Faculty of Art
and Science, St. George Campus ONLY) and convert it into csv files

The data for courses in 2023-2024 was scraped from:
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

NOTICE:
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from os.path import abspath, dirname, exists
from bs4 import BeautifulSoup, Tag
import requests


def download_course(url: str, save_path: str = "") -> None:
    """Save the html file first"""
    with open(save_path, 'wb') as f:
        r = requests.get(url, allow_redirects=True)
        f.write(r.content)


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


def course_block_to_mapping(block: Tag) -> dict[str, str]:
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


def course_in_row(block: Tag) -> str:
    """
    Helper function of html_to_csv. Return course information in a row of csv string.
    """
    block_str = ""
    row_data = course_block_to_mapping(block)
    row = [
        row_data["code"],
        row_data["name"],
        # row_data["prev_code"],
        # row_data["hours"],
        # row_data["detail"],
        row_data["prereq"],
        row_data["coreq"],
        # row_data["recommended_prep"],
        # row_data["exclusions"],
        # row_data["dist_req"],
        row_data["breadth_req"]
    ]
    for i in range(len(row)):
        block_str += row[i]
        if i != len(row) - 1:
            block_str += ":"

    return block_str


def html_to_csv(course_html_path: str, save_dir: str = "", entry_per_file: int = 0) -> None:
    """
    Scrape all the course information from the url specified.
    When entry_per_file is set to -1, data will not be stored in multiple files
    This method uses Beautiful Soup 4 to access DOM element in html.
    """
    with open(course_html_path, 'r') as f:
        # Read content from HTML file first
        html_content = f.read()

        # Use Beautiful Soup to parse and access DOM element
        document = BeautifulSoup(html_content)
        blocks = document.select(".no-break.w3-row.views-row")

        # Save the file into csv files
        number_of_entries = 0
        w, epf = None, -1
        if entry_per_file > 0:
            epf = entry_per_file

        for block in blocks:
            if number_of_entries % epf == 0:
                save_path = f"{save_dir}/{number_of_entries // epf + 1}.csv"
                w = open(save_path, 'w')

            w.write(f"{course_in_row(block)}\n")

            number_of_entries += 1
            if entry_per_file <= 0:
                epf = number_of_entries + 1
            if number_of_entries % epf == 0:
                w.close()


def scrape_course(url: str, course_html_filename: str, save_dirname: str, entry_per_file: int = 0) -> None:
    """Scrape course information."""
    base_path = dirname(abspath(__file__))
    course_html_path = f"{base_path}/{course_html_filename}"
    save_dir = f"{base_path}/{save_dirname}"

    if not exists(course_html_path):
        download_course(url, course_html_path)

    html_to_csv(course_html_path, save_dir, entry_per_file)


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136'],
    #     'extra-imports': ['bs4', 'requests', 'os.path'],
    #     'allowed-io': ['download_course', 'html_to_csv'],
    #     'max-nested-blocks': 4
    # })

    scrape_course("https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug?page=1",
                  "course_information.html", "course_data", 1800)
    