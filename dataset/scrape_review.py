"""SCRAPE_REVIEW
This is a python file that downloads all courses reviews from https://www.uoftindex.ca/

This python file uses course codes from course_data. Please ensure course_data are
downloaded before running this python file.

The generated csv contains the following (10) columns, in the following order:

USER_ID: the id of the user
COURSE_CODE: the code of the course (as displayed on acorn)
REVIEW: integer from 0-10 (original scale 0-5 with an interval of 0.5)


NOTICE:
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from os.path import abspath, dirname, exists
from bs4 import BeautifulSoup, Tag
import requests


def check_website_review(query_url: str) -> str:
    """
    Helper function of get_review_from_url
    Visit the url and return html code of the query_url
    This methods uses requests to view sources code of a webpage at the specified url.
    """
    ...


def get_review_from_block(block: Tag) -> dict[str, int]:
    """Helper function of get_review_from_url to convert html to a mapping"""
    ...


def get_review_from_url(query_url: str) -> list[dict[str, int]]:
    """Helper function of scrape_review. Return a list of reviews from the corresponding url"""
    ...


def review_in_rows(reviews: list[dict[str, int]]) -> str:
    """Helper function of scrape_review. Return a row of csv string"""
    ...




def scrape_review(url: str, course_dirname: str, save_dirname: str, entry_per_file: int = 0) -> None:
    """
    Scrape all course reviews from the url specified.
    When entry_per_file is set to -1, data will not be stored in multiple files
    This method uses Beautiful Soup 4 to access DOM element in html"""
    base_path = dirname(abspath(__file__))
    course_dirname = f"{base_path}/{course_dirname}"
    save_dirname = f"{base_path}/{save_dirname}"
    


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136'],
    #     'extra-imports': ['bs4', 'requests', 'os.path'],
    #     'allowed-io': ['download_course', 'scrape_review'],
    #     'max-nested-blocks': 4
    # })

    scrape_review("https://uoftindex.ca/courses?c=","course_information.html", "course_data", 1800)
    