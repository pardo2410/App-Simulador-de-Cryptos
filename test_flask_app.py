import unittest
from test_base import TestFlaskBase

class TestWeb(TestFlaskBase):
    def test_server_is_on(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_route_index(self):
        response= self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
class TestWeb_Purchase(TestFlaskBase):
    def test_server_is_on(self):
        response = self.client.get("/purchase")
        self.assertEqual(response.status_code, 200)

    def test_route_purchase(self):
        response = self.client.get("/purchase")
        self.assertEqual(response.status_code, 200)

class TestWeb_Status(TestFlaskBase):
    def test_server_is_on(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)

    def test_route_status(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
