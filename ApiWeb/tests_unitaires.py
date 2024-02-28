from base64 import b64encode
import unittest
from unittest.mock import patch
from Launcher import app

class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def get_authenticated_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(f'{username}:{password}'.encode()).decode()
        }

    # test du endpoint '/api/data' 
    def test_get_all_data(self):
        username = 'test'
        password = 'test'
        headers = self.get_authenticated_headers(username, password)
        response = self.app.get('/api/data', headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected behavior

    # test du endpoint '/api/data/<packet_type>'
    def test_filter_data_by_type(self):
        username = 'test'
        password = 'test'
        headers = self.get_authenticated_headers(username, password)
        response = self.app.get('/api/data/DHCPREQUEST', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
