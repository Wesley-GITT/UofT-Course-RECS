"""SCRAPE_REVIEW
This is a python file that downloads all (latest) course reviews and convert it into csv files

These are some website to scrape data from: https://uoftindex.ca/, https://uofthub.ca/

The data for reviews was scraped from: <pending> on 2024/03/23

The generated csv contains the following (10) columns, in the following order:

USER: the user code
CODE: the code of the course (as displayed on acorn)
SCORE: review score given by the user

NOTICE:
It could take a long while to download all the data and convert them into csv files
from the website because the amount of data is SUPER ENORMOUS, so be patient.
"""

from os.path import abspath, dirname, exists
from bs4 import BeautifulSoup, Tag
import requests


def scrape_review(url: str, course_html_filename: str, save_dirname: str, entry_per_file: int = 0) -> None:
    """Scrape review information."""
    ...


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136'],
    #     'extra-imports': ['bs4', 'requests', 'os.path'],
    #     'allowed-io': ['download_course', 'html_to_csv'],
    #     'max-nested-blocks': 4
    # })
    ...
