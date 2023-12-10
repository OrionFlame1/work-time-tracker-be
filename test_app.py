import unittest
from flaskr.app import app
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_admin(self):
        data = {"email": "aditoma123@gmail.com",
                "password": "1234"}

        response = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        print(response.status_code)

        self.assertEqual(response.status_code, 200)

        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
