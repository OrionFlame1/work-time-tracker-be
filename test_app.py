import unittest
import json
from flaskr.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_admin(self):
        data = {"email": "adminnumber1@company.com",
                "password": "admin1"}

        response = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as session:
            session['user_id'] = 5
            response = self.app.get('/employees', content_type='application/json')
            self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as session:
            session['user_id'] = 5
            response = self.app.get('/reports', content_type='application/json')
            self.assertEqual(response.status_code, 200)

        taskCreate = {
            "userId": None,
            "name": "Test",
            "description": "idk",
            "status": None,
            "finish": None
        }

        with self.app.session_transaction() as session:
            session['user_id'] = 5
            response = self.app.post('/task',data=json.dumps(taskCreate), content_type='application/json')
            self.assertEqual(response.status_code, 200)

        taskUpdate = {
            "userId": None,
            "name": "Test1",
            "description": "idk2",
            "status": None,
            "finish": None
        }

        with self.app.session_transaction() as session:
            session['user_id'] = 5
            response = self.app.patch('/task/1', data=json.dumps(taskUpdate), content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_employee(self):
        data = {"email": "employeenumber1@company.com",
                "password": "employee1"}

        response = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as session:
            session['user_id'] = 4
            response = self.app.post('/checkin', content_type='application/json')
            self.assertEqual(response.status_code, 200)

        with self.app.session_transaction() as session:
            session['user_id'] = 4
            response = self.app.post('/checkout', content_type='application/json')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
