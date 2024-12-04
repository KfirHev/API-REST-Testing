import pytest
from Utils.BaseClass import BaseClass
from PageObjects.HomePage import HomePage


@pytest.mark.use_browser
class TestRegisterCustomer(BaseClass):

    @pytest.mark.reset
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
