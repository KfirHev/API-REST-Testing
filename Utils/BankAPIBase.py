import requests
import time
from Utils.BaseClass import BaseClass

# Base URL for the Parabank service
BASE_URL = "http://localhost:8090/parabank/services/bank"

# Base headers used for JSON responses
HEADERS = {
    "accept": "application/json",  # This header specifies that the server should respond with JSON data
    "Content-Type": "application/json"  # This header indicates that the request body contains JSON data
}


class BankAPIBase(BaseClass):
    """Helper class for interacting with the Bank OpenAPI."""

    def get_account_balance(self, account_id):
        """
        Fetches account balance for the specified account.

        Args:
            account_id (int): The ID of the account to fetch balance for.

        Returns:
            float: The account balance.

        Raises:
            HTTPError: If there is an HTTP error while fetching the account balance.
            ValueError: If the balance key is missing in the response.
            Exception: If any other unexpected error occurs.
        """
        try:
            response = requests.get(f"{BASE_URL}/accounts/{account_id}", headers=HEADERS)
            response.raise_for_status()

            account_info = response.json()
            if 'balance' not in account_info:
                raise ValueError("Balance key not found in the response.")
            return account_info['balance']
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {http_err}")
        except ValueError as e:
            raise ValueError(f"Failed to retrieve account balance: {e}. Response: {response.text}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching the account balance: {e}")

    def create_new_account(self, customer_id, account_type, source_account_id):
        """
        Creates a new account for a given customer.

        Args:
            customer_id (int): ID of the customer.
            account_type (int): Type of account to create (e.g., 1 for CHECKING).
            source_account_id (int): ID of the funding source account.

        Returns:
            int: ID of the newly created account.

        Raises:
            HTTPError: If the account creation request fails.
            ValueError: If the response does not contain an account ID.
        """
        log = self.get_logger()
        log.info(f"Creating new account for customer {customer_id} with type {account_type}")

        try:
            response = requests.post(
                f"{BASE_URL}/createAccount",
                headers=HEADERS,
                params={
                    "customerId": customer_id,
                    "newAccountType": account_type,
                    "fromAccountId": source_account_id
                }
            )
            response.raise_for_status()

            account_data = response.json()
            account_id = account_data.get('id')
            if account_id is None:
                log.error("Failed to create account: 'id' field missing in response.")
                raise ValueError("Account ID missing in response")


            # Non-verbose log: only log a success message with the new account ID
            log.info(f"New account created with ID: {account_id}")
            return account_id

        except requests.exceptions.HTTPError as http_err:
            log.error(f"HTTP error occurred during account creation: {http_err}")
            raise
        except Exception as e:
            log.error(f"An error occurred while creating the new account: {e}")
            raise

    def deposit_to_account(self, account_id, amount):
        """
        Performs deposit operation on specified account.

        Args:
            account_id (int): The ID of the account to deposit into.
            amount (float): The amount to deposit.

        Returns:
            str: The response text from the deposit operation.

        Raises:
            HTTPError: If the deposit request fails.
            Exception: If any other unexpected error occurs.
        """
        try:
            response = requests.post(f"{BASE_URL}/deposit", headers=HEADERS,
                                     params={"accountId": account_id, "amount": amount})
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred during deposit: {http_err}")
        except Exception as e:
            raise Exception(f"An error occurred while depositing to the account: {e}")

    def withdraw_from_account(self, account_id, amount):
        """
        Performs withdrawal operation on specified account.

        Args:
            account_id (int): The ID of the account to withdraw from.
            amount (float): The amount to withdraw.

        Returns:
            str: The response text from the withdrawal operation.

        Raises:
            HTTPError: If the withdrawal request fails.
            Exception: If any other unexpected error occurs.
        """
        try:
            response = requests.post(f"{BASE_URL}/withdraw", headers=HEADERS,
                                     params={"accountId": account_id, "amount": amount})
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred during withdrawal: {http_err}")
        except Exception as e:
            raise Exception(f"An error occurred while withdrawing from the account: {e}")

    def billpay(self, account_id, amount, name, street, city, state, zip_code, phone_number, account_number):
        """
        Performs billpay operation on the specified account.

        Args:
            account_id (int): The account ID for the bill payment.
            amount (float): The amount to pay.
            name (str): The name of the bill recipient.
            street (str): The street address of the recipient.
            city (str): The city of the recipient.
            state (str): The state of the recipient.
            zip_code (str): The zip code of the recipient.
            phone_number (str): The phone number of the recipient.
            account_number (str): The account number for the payment.

        Returns:
            dict: The response JSON data from the billpay operation.

        Raises:
            HTTPError: If the billpay request fails.
            Exception: If any other unexpected error occurs.
        """
        params = {
            'accountId': account_id,
            'amount': amount
        }

        data = {
            "name": name,
            "address": {
                "street": street,
                "city": city,
                "state": state,
                "zipCode": zip_code
            },
            "phoneNumber": phone_number,
            "accountNumber": account_number
        }

        try:
            response = requests.post(
                f"{BASE_URL}/billpay",
                headers=HEADERS,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred during billpay: {http_err}")
        except Exception as e:
            raise Exception(f"An error occurred while performing billpay: {e}")

    def get_customer_details(self, account_id):
        """
        Fetches customer details based on account ID.

        Args:
            account_id (int): The ID of the account whose customer details are to be fetched.

        Returns:
            dict: The customer details.

        Raises:
            HTTPError: If the request to fetch customer details fails.
            ValueError: If customer details are not found.
            Exception: If any other unexpected error occurs.
        """
        try:
            response = requests.get(f"{BASE_URL}/customers/{account_id}", headers=HEADERS)
            response.raise_for_status()

            account_info = response.json()
            if not account_info:
                raise ValueError("Accounts not found in the response.")
            return account_info
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred while retrieving customer details: {http_err}")
        except ValueError as e:
            raise ValueError(f"Failed to retrieve customer details: {e}. Response: {response.text}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching customer details: {e}")

    def get_account_by_id(self, account_id):
        """
        Fetches account details by account ID.

        Args:
            account_id (int): The ID of the account to fetch.

        Returns:
            dict: The account details.

        Raises:
            HTTPError: If the request to fetch account details fails.
            ValueError: If account details are not found.
            Exception: If any other unexpected error occurs.
        """
        try:
            response = requests.get(f"{BASE_URL}/accounts/{account_id}", headers=HEADERS)
            response.raise_for_status()

            account_info = response.json()
            if not account_info:
                raise ValueError("Accounts not found in the response.")
            return account_info
        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTP error occurred while retrieving account: {http_err}")
        except ValueError as e:
            raise ValueError(f"Failed to retrieve account details: {e}. Response: {response.text}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching account details: {e}")

    def get_loan_approval(self, customer_id, amount, down_payment, source_account_id):
        """
        Requests a loan approval for the customer.

        Args:
            customer_id (int): The ID of the customer requesting the loan.
            amount (float): The loan amount requested.
            down_payment (float): The down payment for the loan.
            source_account_id (int): The account ID from which the loan payment is funded.

        Returns:
            bool: Whether the loan was approved.

        Raises:
            HTTPError: If the request to fetch account details fails.
            ValueError: If account details are not found.
            Exception: If any other unexpected error occurs.
        """

        log = self.get_logger()
        log.info(f"Requesting a loan of {amount} for customer {customer_id}, down payment: {down_payment}")

        try:
            response = requests.post(
                f"{BASE_URL}/requestLoan",
                headers=HEADERS,
                params={
                    "customerId": customer_id,
                    "amount": amount,
                    "downPayment": down_payment,
                    "fromAccountId": source_account_id
                }
            )
            response.raise_for_status()
            approval_response = response.json()
            #  If the 'approved' key is not present, it returns False as a default value.
            return approval_response.get('approved', False)
        except requests.exceptions.HTTPError as http_err:
            log.error(f"HTTP error occurred while requesting loan approval: {http_err}")
            raise
        except Exception as e:
            log.error(f"An error occurred while requesting loan approval: {e}")
            raise

    def buy_position(self, source_account, pos_name, pos_symbol, number_of_shares, share_price):

        log = self.get_logger()
        log.info(f"Requesting a to buy {number_of_shares} of {pos_name} shares for customer {self.CUSTOMER_ID[0][0]}, "
                 f"funds transfer from account: {source_account}")

        try:
            response = requests.post(
                f"{BASE_URL}/customers/{self.CUSTOMER_ID[0][0]}/buyPosition",
                headers=HEADERS,
                params={
                    "accountId": source_account,
                    "name": pos_name,
                    "symbol": pos_symbol,
                    "shares": number_of_shares,
                    "pricePerShare": share_price,
                }
            )
            response.raise_for_status()
            approval_response = response.json()
            #  If the 'approved' key is not present, it returns False as a default value.
            return approval_response
        except requests.exceptions.HTTPError as http_err:
            log.error(f"HTTP error occurred while requesting buying position: {http_err}")
            raise
        except Exception as e:
            log.error(f"An error occurred while requesting to buy position: {e}")
            raise

    def clean_database(self):
        """Cleans the database by sending a POST request."""
        log = self.get_logger()
        try:
            response = requests.post(f"{BASE_URL}/cleanDB", headers=HEADERS)
            response.raise_for_status()
            log.info(f"Database cleaned successfully: {response}")
            return response.text
        except requests.exceptions.HTTPError as http_err:
            log.error(f"HTTP error occurred while cleaning database: {http_err}")
            raise
        except Exception as e:
            log.error(f"An error occurred while cleaning the database: {e}")
            raise
