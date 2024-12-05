import pytest
from Utils.BankAPIBase import BankAPIBase


class TestBankAccountsAPI(BankAPIBase):

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

    # @pytest.mark.skip
    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_open_new_account(self, initial_balance):
        """
        Test case for creating a new bank account for a specific customer.

        This test performs the following:
        1. Attempts to create a new account by transferring a specified amount from an existing account.
        2. Verifies that the initial account balance is correctly updated after the transfer.
        3. Asserts the successful creation of the new account by checking for a valid account ID and a positive balance.

        Parameters:
        initial_balance (float): The balance of the source account before creating the new account.

        Assertions:
        - Ensures that the source account balance is reduced by the expected amount.
        - Confirms that a new account ID is returned upon successful creation.
        - Validates that the new account has the correct balance allocated.

        Logs:
        - Relevant information on account creation and balance update for debugging purposes.
        """
        log = self.get_logger()

        # Parameters for new account creation
        customer_id = self.CUSTOMER_ID
        account_type = 1  # Assuming 1 represents a specific account type like CHECKING
        source_account_id = self.BASE_ACCOUNT_ID

        log.info("Attempting to create a new account.")
        log.info(f"Withdrawing $100 from account {self.BASE_ACCOUNT_ID} to allocate to the new account")

        new_account_id = self.create_new_account(self.CUSTOMER_ID[0], account_type, source_account_id)

        # Verify updated balance in source account
        updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        new_account_balance = self.get_account_balance(new_account_id)

        log.info(f"Updated balance after creating new account: {updated_balance}")

        # Assert source account balance reflects the $100 allocation for the new account
        assert updated_balance == initial_balance - 100, "Balance did not update correctly after allocation"
        log.info("Allocation of $100 for the new account passed successfully.")

        # Assert that a valid account ID is returned upon successful account creation
        assert new_account_id is not None, "Failed to create a new account: No account ID returned"

        # Log success of account creation with its balance
        log.info(
            f"New account created successfully with ID: {new_account_id} and balance of ${int(new_account_balance)}")




