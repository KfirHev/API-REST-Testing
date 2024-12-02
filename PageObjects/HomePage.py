from Utils.BaseClass import BaseClass
from selenium.webdriver.common.by import By


class HomePage(BaseClass):
    """Page object model for the Home Page, handling user interactions like login and registration."""

    # Locators for elements on the Home Page
    l_register_link = (By.LINK_TEXT, "Register")
    l_user_name = (By.CSS_SELECTOR, "input[name='username']")
    l_user_pw = (By.CSS_SELECTOR, "input[name='password']")
    l_login_btn = (By.CSS_SELECTOR, "input[value='Log In']")
    l_first_name = (By.ID, "customer.firstName")
    l_last_name = (By.ID, "customer.lastName")
    l_address = (By.ID, "customer.address.street")
    l_city = (By.ID, "customer.address.city")
    l_state = (By.ID, "customer.address.state")
    l_zip = (By.ID, "customer.address.zipCode")
    l_phone = (By.ID, "customer.phoneNumber")
    l_ssn = (By.ID, "customer.ssn")
    l_form_user_name = (By.ID, "customer.username")
    l_form_pwd = (By.ID, "customer.password")
    l_form_confirm_pw = (By.ID, "repeatedPassword")
    l_register_btn = (By.CSS_SELECTOR, "input[value='Register']")

    def __init__(self, driver):
        """
        Initializes the HomePage object with the WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

    def fill_register_form(self):
        """
        Fills out and submits the registration form with pre-defined test data.

        This simulates a user registering on the platform by providing test inputs
        for all required fields.
        """
        # Click the "Register" link to navigate to the registration form
        self._driver.find_element(*self.l_register_link).click()

        # Fill out the form fields with predefined data
        self._driver.find_element(*self.l_first_name).send_keys("Luke")
        self._driver.find_element(*self.l_last_name).send_keys("Skywalker")
        self._driver.find_element(*self.l_address).send_keys("123 Happy St")
        self._driver.find_element(*self.l_city).send_keys("Mos Eisley")
        self._driver.find_element(*self.l_state).send_keys("Outer Rim")
        self._driver.find_element(*self.l_zip).send_keys("45678")
        self._driver.find_element(*self.l_phone).send_keys("555-1234")
        self._driver.find_element(*self.l_ssn).send_keys("987-65-4321")
        self._driver.find_element(*self.l_form_user_name).send_keys("JediMasterLuke")
        self._driver.find_element(*self.l_form_pwd).send_keys("Realpass889$")
        self._driver.find_element(*self.l_form_confirm_pw).send_keys("Realpass889$")

        # Submit the registration form
        self._driver.find_element(*self.l_register_btn).click()

    def login(self):
        """
        Logs in the user by filling in the username and password fields and clicking the login button.

        This simulates a user logging into the platform with predefined test credentials.
        """
        # Enter username and password
        self._driver.find_element(*self.l_user_name).send_keys("JediMasterLuke")
        self._driver.find_element(*self.l_user_pw).send_keys("Realpass889$")

        # Click the login button to submit the form
        self._driver.find_element(*self.l_login_btn).click()
