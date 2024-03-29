"""
This is a helper module for scrape_review and scrape_crouse.
"""

from bs4 import Tag
import requests

def get_url_html(url: str) -> str:
    """Get html content of a webpage at specified url."""
    r = requests.get(url, allow_redirects=True)
    return r.content


def in_a_row(mapping: dict[str, str], order: list, delimiter: str = ":") -> str:
    """
    Return course information in a row of csv string.
    
    Precondition:
      - all(key in mapping for key in order)
    """
    block_str = ""
    for key in order:
        block_str += mapping[key] + delimiter

    return block_str[:len(block_str) - 1]


def get_text_from_html_element(block: Tag, css_selector: str) -> str:
    """
    Extract text from an html element.
    If the element is not found, return an empty string.
    """
    elements = block.select(css_selector)
    if len(elements) == 0:
        return ""
    else:
        return elements[0].get_text().strip().replace("\n", "")


def get_info_from_html(block: Tag, css_selector_mapping: dict[str, str]) -> dict[str, str]:
    """Convert html to a mapping of information."""
    data = {}
    for key in css_selector_mapping:
        data[key] = get_text_from_html_element(block, css_selector_mapping[key])

    return data