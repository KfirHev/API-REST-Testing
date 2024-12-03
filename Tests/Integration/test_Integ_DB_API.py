import time
import pytest
from Utils.BankAPIBase import BankAPIBase
from PageObjects.HomePage import HomePage


class TestBankDBAPI(BankAPIBase):
    """
    Test class for Bank Database API interactions.
    """
    @pytest.mark.reset
    def test_clean_db(self):
        """
        Test to clean the database.

        Steps:
        1. Call `clean_database` to clean the database.
        """
        log = self.get_logger()
        # Perform database cleanup
        self.clean_database()
        log.info("Database cleaned successfully.")

        time.sleep(10)   # Sleep until DB is initialized

    @pytest.mark.reset
    @pytest.mark.use_browser
    def test_register_and_login(self):
        """
        Test user registration and login functionality.

        Steps:
        Fill out the registration form on the home page and register new account
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        # Register a new user
        home_page.fill_register_form()

