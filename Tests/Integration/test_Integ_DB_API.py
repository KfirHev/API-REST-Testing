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

