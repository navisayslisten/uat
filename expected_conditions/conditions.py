"""Custom expected conditions."""

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # noqa
from selenium.webdriver.support.ui import WebDriverWait

from utils import utils as ut

class url_in_new_tab_matches:  # noqa
    """Wait until new tab contains redirected url."""

    def __init__(self, url):
        """Init escpected condition."""
        self.url = url

    def __call__(self, driver):
        """Test if url matches."""
        return driver.current_url == self.url

class table_has_data:  # noqa
    """Wait until table has data."""

    def __init__(self, table):
        """Init expected condition."""
        self.table = table

    def __call__(self, driver):
        """Test if table has more than one column."""
        tds = self.table.table.find_elements_by_tag_name('td')

        return len(tds) > 1

class element_is_clickable:  # noqa
    """Wait element is clickable."""

    def __init__(self, element):
        """Init expected condition."""
        self.element = element

    def __call__(self, driver):
        """Test if element is clickable."""
        return all([self.element.is_enabled(), self.element.is_displayed()])

class table_cell_updated: # noqa
    """Wait until cell data has updated."""

    def __init__(self, table, header, expected, table_attr, row_number):
        """Init expected condition.

        :table: Table component
        :header: Name of the table header
        :expected: Expected value cell value should be
        :table_attr: Name of the attr of table reference, usually 'table'
        :row_number: Row number to retrieve
        """
        self.table = table
        self.header = header
        self.expected = expected
        self.table_attr = table_attr
        self.row_number = row_number

    def __call__(self, driver):
        """Test if col value has updated."""
        row = ut.get_table_row(
            self.table,
            self.table_attr,
            row_number=self.row_number
        )

        actual = getattr(row, self.header)
        actual = ' '.join([string.strip() for string in actual.split()])

        return actual == self.expected

class sorting_arrow_up: # noqa
    """Wait until sorting arrow is pointing up."""

    def __init__(self, element):
        """Init expected condition.

        :param element: Selenium WebElement object
        """
        self.element = element

    def __call__(self, driver):
        """Test is arrow is pointing up."""
        return 'fa-arrow-up' in self.element.get_attribute('class')

class sorting_arrow_down: # noqa
    """Wait until sorting arrow is pointing down."""

    def __init__(self, element):
        """Init expected condition.

        :param element: Selenium WebElement object
        """
        self.element = element

    def __call__(self, driver):
        """Test if arrow is pointing down."""
        return 'fa-arrow-down' in self.element.get_attribute('class')


class modal_finished_closing: # noqa
    """Wait until modal finished closing."""

    def __init__(self, element_id):
        """Init expected condition.

        :param element_id: ID of DOM element
        """
        self.element_id = element_id

    def __call__(self, driver):
        """Test if modal has closed."""
        # Required for Firefox
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, 'modal-backdrop fade')
                )
            )
        except NoSuchElementException:
            pass

        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.ID, self.element_id)
                )
            )
        except NoSuchElementException:
            pass

        return True
