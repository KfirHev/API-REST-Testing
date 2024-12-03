from Utils.BaseClass import BaseClass
from locust import HttpUser, task, between
from faker import Faker
import random

BASE_URL = "http://localhost:8090/parabank/services/bank"


class BankAPIPerformance(HttpUser, BaseClass):
    """
    Locust class to load test the BankAPIBase methods, inheriting reusable data and logic from BaseClass.
    """
    wait_time = between(1, 5)  # Wait between requests (randomized to simulate real users)

    def __init__(self, *args, **kwargs):
        # Initialize the customer_id, account_id, and source_account_id from BaseClass class-level attributes
        super().__init__(*args, **kwargs)
        self.customer_id = self.CUSTOMER_ID[0][0]  # Assuming the first customer ID
        self.account_id = random.choice(self.ACCOUNT_ID_LIST)[0]  # Random account ID from the list
        self.source_account_id = random.choice(self.ACCOUNT_ID_LIST)[0]  # Random source account ID from the list

    @task(3)
    def get_account_balance(self):
        self.client.get(f"{BASE_URL}/accounts/{self.account_id}", headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    @task(1)
    def create_new_account(self):
        self.client.post(
            f"{BASE_URL}/createAccount",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            params={
                "customerId": self.customer_id,
                "newAccountType": 1,  # Assuming 1 is CHECKING
                "fromAccountId": self.source_account_id
            }
        )

    @task(3)
    def deposit_to_account(self):
        self.client.post(
            f"{BASE_URL}/deposit",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            params={
                "accountId": self.account_id,
                "amount": random.randint(100, 1000)  # Random deposit amount
            }
        )

    @task(2)
    def withdraw_from_account(self):
        self.client.post(
            f"{BASE_URL}/withdraw",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            params={
                "accountId": self.account_id,
                "amount": random.randint(50, 500) # Random withdrawal amount
            }
        )

    @task(1)
    def billpay(self):

        fake = Faker()
        name = fake.name()
        street = fake.street_address()
        city = fake.city()
        state = fake.state()
        zip_code = fake.zipcode()
        phone_number = fake.phone_number()
        account_number = fake.random_int(15000, 30000)

        self.client.post(
            f"{BASE_URL}/billpay",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            params={"accountId": self.account_id, "amount": random.randint(100, 500)},
            json={
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
        )

    @task(2)
    def get_customer_details(self):
        self.client.get(f"{BASE_URL}/customers/{self.customer_id}", headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    @task(1)
    def get_account_by_id(self):
        self.client.get(f"{BASE_URL}/accounts/{self.account_id}", headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    @task(1)
    def get_loan_approval(self):
        self.client.post(
            f"{BASE_URL}/requestLoan",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            },
            params={
                "customerId": self.customer_id,
                "amount": 200,
                "downPayment": 20,
                "fromAccountId": self.source_account_id
            }
        )
