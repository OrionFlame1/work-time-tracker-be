import unittest
import requests
from jsonify.convert import jsonify


class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000"

    def login_succed(self):
        resp = requests.post(self.URL+"/login", None, jsonify({"email": "employeenumber1@company.com", "password": "employee1"}))
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    tester = TestAPI()

    tester.login_succed()