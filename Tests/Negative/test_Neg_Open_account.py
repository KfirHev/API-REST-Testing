import pytest
from Utils.BankAPIBase import BankAPIBase


class TestBankAccountsNegativeAPI(BankAPIBase):

    @pytest.fixture
    def initial_balance(self):
        """Fixture to get the initial balance of the sample account before each test."""
        log = self.get_logger()
        try:
            initial_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
            log.info(f"Initial balance for account {self.BASE_ACCOUNT_ID}: {initial_balance}")
            return initial_balance
        except ValueError as e:
            # Log the error when get_account_balance fails
            log.error(f"Failed to retrieve initial balance: {e}")
            # Optionally, re-raise the exception if you want the test to fail
            raise

    @pytest.mark.Negative
    def test_open_new_account(self, initial_balance):
        """
        Test case for creating a new bank account for a specific customer.

        This test performs the following:
        1. Attempts to create a new account using an invalid source account.
        2. Verifies that the source account balance remains unchanged after the failure.
        3. Asserts the error response contains the expected status code and details.

        Parameters:
        initial_balance (float): The balance of the source account before attempting the operation.

        Assertions:
        - Ensures that the source account balance is not reduced due to the failure.
        - Confirms that the response contains error details with the expected status code and message.

        Logs:
        - Relevant information on account creation and balance verification for debugging purposes.
        """
        log = self.get_logger()

        # Parameters for new account creation
        customer_id = self.CUSTOMER_ID
        account_type = 1  # Assuming 1 represents a specific account type like CHECKING
        source_account_id = 1515512  # INVALID Account

        log.info("Attempting to create a new account with invalid source account.")
        log.info(f"Using customer ID: {customer_id}, account type: {account_type}, source account: {source_account_id}")

        # Call the API method to attempt new account creation
        result = self.create_new_account(customer_id[0], account_type, source_account_id)

        # Verify the source account balance remains unchanged
        updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Source account balance after attempt: {updated_balance}")

        assert updated_balance == initial_balance, "Balance updated despite failed account creation"
        log.info("Source account balance is unchanged as expected after failure.")

        # # Assert that the response contains error details
        # assert isinstance(response, dict), "Response is not a dictionary"
        # assert "error" in response, "'error' key missing in response"
        # assert "details" in response, "'details' key missing in response"

        # Validate the error details
        assert '400' in result['error'], f"Unexpected error message: {result['error']}"
        assert "Could not create new account" in result['details'], f"Error details mismatch: {result['details']}"

        log.info(f"Account creation failed as expected with {result['error']} and details are:"
                 f"{result['details']}")

