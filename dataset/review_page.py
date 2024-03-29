"""
This is a helper module for scrape_review to automatically create and navigate a web browser
to quercus and then the evaluation page.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


class EvalPage:
    """A webdriver instance to scrape review from UofT evaluation page"""

    driver: webdriver.Chrome

    def __init__(self, utorid: str, passwd: str, max_page: int = 10) -> None:
        """
        Initialize an evaluation page in a chrome browser and configure it.
        max_page is the maximum number of items to display at once.
        
        Preconditions:
          - max_page in [5, 10, 15, 20, 25, 50, 100]
        """

        # initialize a google chrome browser
        options = Options()
        # options.add_argument("--headless")
        browser = webdriver.Chrome(executable_path="chromedriver", options=options)
        browser.implicitly_wait(10)
        # browser.minimize_window()
        browser.get("https://q.utoronto.ca")
        self.driver = browser

        # login into quercus
        self.select("#username").send_keys(utorid)
        self.select("#password").send_keys(passwd)
        self.select("#login-btn").click()

        # entering course evaluation pages
        self.select("#context_external_tool_2015_menu_item").click()
        self.select("#section-tabs > li:nth-child(3)").click()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id*='tool_content']"))
        )
        self.select("#launcherElements tbody > tr:nth-child(3) a").click()
        self.driver.switch_to.window(self.driver.window_handles[1])

        # set the maximum number of items to the specified value
        mapping = {5: "0", 10: "1", 15: "2", 20: "3", 25: "4", 50: "5", 100: "6"}
        select = Select(self.select("#fbvGridPageSizeSelectBlock select"))
        select.select_by_index(mapping[max_page])
        self.wait()

    def get_num_records(self) -> int:
        """Return the total number of records of evaluations"""
        return int(self.select("#fbvGridNbItemsTotalLvl1").text[6:].strip())

    def get_num_pages(self) -> int:
        """Return the total number of pages"""
        return int(self.select("#fbvGridPagingContentHolderLvl1 tbody>tr:nth-child(1)>td:nth-child(5)").text.strip())

    def select(self, css_selector: str) -> WebElement:
        """Select the specified html element"""
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def wait(self) -> None:
        """Wait until the datais loaded"""
        WebDriverWait(self.driver, 600, 0.1).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#waitMachineID"))
        )

    def get_data(self, num_page: int) -> str:
        """Get data in html form"""
        if num_page > self.get_num_pages():
            return "<!DOCTYPE html></html><body></body></html>"

        input_dom = self.select("#gridPaging__getFbvGrid")
        input_dom.clear()
        input_dom.send_keys(str(num_page))
        input_dom.send_keys(Keys.ENTER)
        self.wait()
        table_html = self.select("#fbvGrid").get_attribute("outerHTML")
        return f"<!DOCTYPE html></html><body>{table_html}</body></html>"


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ["selenium", "selenium.webdriver.common.keys", "selenium.webdriver.remote.webelement",
                          "selenium.webdriver.chrome.options", "selenium.webdriver.common.by",
                          "selenium.webdriver.support", "selenium.webdriver.support.ui"],
        'max-nested-blocks': 4
    })
