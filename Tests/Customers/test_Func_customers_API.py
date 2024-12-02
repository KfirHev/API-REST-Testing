import pytest
from faker import Faker
from Utils.BankAPIBase import BankAPIBase


class TestBankCustomersAPI(BankAPIBase):
    @pytest.fixture()
    def initial_balance(self):
        """Fixture to get the initial balance of the sample account before each test.

        Steps:
        1. Retrieve the account balance using `get_account_balance`.
        2. Return the balance for use in tests.
        """
        log = self.get_logger()
        # Get initial balance of the account and log the information
        init_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Initial balance for account {self.BASE_ACCOUNT_ID}: {init_balance}")
        return init_balance

    #@pytest.mark.skip
    @pytest.mark.Regression
    def test_get_customer_detail(self):
        """
        Test to retrieve customer details and validate key fields.
        Skipped due to being marked as such.

        Steps:
        1. Call `get_customer_details` with a valid customer ID.
        2. Assert that the response is not None.
        """
        log = self.get_logger()
        # Get customer details and log them
        response = self.get_customer_details(self.CUSTOMER_ID[0][0])

        # Validate response is not None
        assert response is not None
        log.info(f"User Details - ID: {response.get('id')}, First Name: {response.get('firstName')}, "
                 f"Last Name: {response.get('lastName')}, Street Address: {response.get('address', {}).get('street')}, "
                 f"City: {response.get('address', {}).get('city')}, State: {response.get('address', {}).get('state')}, "
                 f"ZIP Code: {response.get('address', {}).get('zipCode')}, Phone Number: {response.get('phoneNumber')}, "
                 f"SSN: {response.get('ssn')}")

    # @pytest.mark.skip
    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_deposit_and_balance_update(self, initial_balance):
        """
        Tests deposit functionality and verifies the balance is updated correctly.
        Ensures the updated balance matches the expected amount after deposit.

        Steps:
        1. Call `deposit_to_account` to deposit the specified amount.
        2. Retrieve the updated account balance using `get_account_balance`.
        3. Assert that the updated balance is equal to the initial balance + deposit amount.
        """
        log = self.get_logger()
        deposit_amount = 5000

        # Log deposit attempt
        log.info(f"Depositing {deposit_amount} to account {self.BASE_ACCOUNT_ID}")
        # Perform deposit
        self.deposit_to_account(self.BASE_ACCOUNT_ID, deposit_amount)

        # Verify updated balance
        updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Updated balance after deposit: {updated_balance}")

        # Assert that the updated balance is correct
        assert updated_balance == initial_balance + deposit_amount, "Balance did not update correctly after deposit"
        log.info("Deposit and balance update test passed successfully.")

    #@pytest.mark.skip
    @pytest.mark.Sanity
    @pytest.mark.Regression
    def test_withdrawal_and_balance_update(self, initial_balance):
        """
        Tests withdrawal functionality and verifies the balance is updated correctly.
        Ensures the updated balance matches the expected amount after withdrawal.

        Steps:
        1. Call `withdraw_from_account` to withdraw the specified amount.
        2. Retrieve the updated account balance using `get_account_balance`.
        3. Assert that the updated balance is equal to the initial balance - withdrawal amount.
        """
        log = self.get_logger()
        withdraw_amount = 200

        # Log withdrawal attempt
        log.info(f"Withdrawing {withdraw_amount} from account {self.BASE_ACCOUNT_ID}")
        # Perform withdrawal
        self.withdraw_from_account(self.BASE_ACCOUNT_ID, withdraw_amount)

        # Verify updated balance
        updated_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Updated balance after withdrawal: {updated_balance}")

        # Assert that the updated balance is correct
        assert updated_balance == initial_balance - withdraw_amount, "Balance did not update correctly after withdrawal"
        log.info("Withdrawal and balance update test passed successfully.")

    #@pytest.mark.skip
    @pytest.mark.Regression
    def test_deposit_and_withdrawal(self, initial_balance):
        """
        Tests a sequence of deposit and withdrawal, ensuring the balance reflects both transactions.
        Validates the final balance after deposit and withdrawal.

        Steps:
        1. Perform the deposit using `deposit_to_account`.
        2. Perform the withdrawal using `withdraw_from_account`.
        3. Retrieve the final account balance using `get_account_balance`.
        4. Assert that the final balance matches the expected final balance.
        """
        log = self.get_logger()
        deposit_amount = 1000
        withdraw_amount = 200

        # Log deposit and withdrawal attempts
        log.info(f"Depositing {deposit_amount} to account {self.BASE_ACCOUNT_ID}")
        self.deposit_to_account(self.BASE_ACCOUNT_ID, deposit_amount)
        log.info(f"Withdrawing {withdraw_amount} from account {self.BASE_ACCOUNT_ID}")
        self.withdraw_from_account(self.BASE_ACCOUNT_ID, withdraw_amount)

        # Verify final balance
        final_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        expected_balance = initial_balance + deposit_amount - withdraw_amount

        log.info(f"Final balance after deposit and withdrawal: {final_balance}")
        # Assert the final balance is correct
        assert final_balance == expected_balance, "Final balance is incorrect after deposit and withdrawal"
        log.info("Deposit and withdrawal test passed successfully.")

    #@pytest.mark.skip
    @pytest.mark.Regression
    def test_pay_bill(self, initial_balance):
        """
        Tests a sequence of bill payment with fake data.
        Verifies that the bill payment process works and the final balance is updated correctly.

        Steps:
        1. Generate fake user data using `Faker`.
        2. Call `billpay` with the generated fake data and account information.
        3. Retrieve the approval response and assert that the payee name matches the generated name.
        4. Calculate the expected balance: initial balance - bill amount.
        5. Retrieve the final balance after payment.
        6. Assert that the final balance matches the expected balance.
        """
        fake = Faker()  # Generate fake data for testing
        log = self.get_logger()
        bill_amount = 350  # Amount for the bill payment

        # Generate fake user data
        name = fake.name()
        street = fake.street_address()
        city = fake.city()
        state = fake.state()
        zip_code = fake.zipcode()
        phone_number = fake.phone_number()
        account_number = fake.random_int(15000, 30000)
        expected_balance = initial_balance - bill_amount

        # Log the payment attempt
        log.info(f"Paying {bill_amount} from account {self.BASE_ACCOUNT_ID} to {name}")

        # Perform bill payment
        approval = self.billpay(self.BASE_ACCOUNT_ID, bill_amount,
                                name, street, city, state, zip_code,
                                phone_number, account_number)
        payee = approval.get("payeeName")
        assert payee == name
        log.info(f"Bill was paid to {payee}")

        # Verify final balance after bill payment
        final_balance = self.get_account_balance(self.BASE_ACCOUNT_ID)
        log.info(f"Final balance after paying the bill: {final_balance}")
        assert final_balance == expected_balance, "Final balance is incorrect after bill payment"

        # Log the approval details
        log.info(f"Payment approved: {approval}")

    @pytest.mark.parametrize(
        "source_account, pos_name, pos_symbol, number_of_shares, share_price",
        [
            (13455, 'Apple', 'AAPL', 225, 5),  # Sufficient funds for purchase
            pytest.param(13788, 'Apple', 'AAPL', 225, 100,
                         marks=pytest.mark.xfail(reason="Expected to fail due to insufficient funds", strict=False)),
        ]
    )
    #@pytest.mark.skip
    @pytest.mark.Regression
    def test_buy_position(self,source_account, pos_name, pos_symbol, number_of_shares, share_price):
        """
        Tests the ability to buy a position.

        Steps:
        1. Calculate the expected cost of the position.
        2. Attempt to buy the position using the provided account and details.
        3. Retrieve and assert the final account balance matches the expected value.
        """
        log = self.get_logger()
        initial_balance = self.get_account_balance(source_account)

        # Perform the action
        self.buy_position(source_account, pos_name, pos_symbol, number_of_shares, share_price)

        # Validate the final balance
        final_balance = self.get_account_balance(source_account)
        expected_balance = initial_balance - (number_of_shares * share_price)
        assert final_balance == expected_balance, (
            f"Final balance is incorrect. Expected: {expected_balance}, Got: {final_balance}"
        )
