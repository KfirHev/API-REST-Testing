import pytest
from Utils.BankAPIBase import BankAPIBase


class TestBankLoanAPI(BankAPIBase):
    """
    Test class for verifying the loan functionality in the bank API.

    Inherits from the BankAPIBase, which contains utility methods for interacting
    with the bank's API and database.
    """

    @pytest.mark.parametrize(
        "loan_amount, down_payment, expected_approval",
        [
            (1000, 100, True),  # Sufficient funds for loan approval
            (5000, 500, True),  # Another valid case with larger amounts
            (20000000, 500000, False)  # (Negative) Expected to not get loan approval due to insufficient funds
        ]
    )
    @pytest.mark.Regression
    def test_valid_loan(self, loan_amount, down_payment, expected_approval):
        """
        Test case for approving or rejecting a loan request and verifying account balance and loan approval status.

        Args:
            loan_amount (int): The amount of loan requested.
            down_payment (int): The down payment for the loan.
            expected_approval (bool): Expected result of loan approval (True for pass, False for expected failure).
        """
        # Initialize logger
        log = self.get_logger()

        # Step 1: Get the initial balance of the account before applying for the loan
        initial_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Initial balance for account {self.BASE_ACCOUNT_ID}: {initial_balance}")

        # Step 2: Apply for a loan
        approval_status = self.get_loan_approval(self.CUSTOMER_ID[0][0], loan_amount, down_payment,
                                                 self.BASE_ACCOUNT_ID)

        # Assert the loan approval status matches expected approval
        assert approval_status == expected_approval, f"Loan approval status {approval_status} did not match expected {expected_approval}"

        # If approval is successful, proceed with further assertions
        if approval_status:
            # Step 3: Retrieve the new loan account if loan is approved
            new_loan_account = self.execute_db_query("SELECT MAX(ID) FROM PUBLIC.ACCOUNT")
            log.info(f"New loan account created with ID: {new_loan_account[0][0]}")

            # Retrieve the account details and perform assertions
            new_account_info = self.get_account_by_id(new_loan_account[0][0])
            assert new_account_info.get(
                'type') == 'LOAN', f"Expected account type 'LOAN', but got {new_account_info.get('type')}"
            assert new_account_info.get(
                'balance') == loan_amount, f"Expected loan balance of {loan_amount}, but got {new_account_info.get('balance')}"
            log.info(
                f"Loan account created successfully. Type: {new_account_info.get('type')}, Balance: {new_account_info.get('balance')}")

            # Step 4: Verify the balance update after the loan approval
            updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
            assert updated_balance == initial_balance - down_payment, "Balance did not update correctly after loan approval"
            log.info(f"Balance updated correctly after loan approval. New balance: {updated_balance}")
        else:
            updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
            assert updated_balance == initial_balance, "Balance shouldn't be changed since load was not approved "
            log.info(f"Balance stay the same since loan was not approved: {updated_balance}")

        log.info("Loan test and down payment verification passed successfully.")
