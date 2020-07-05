from flask import Flask
from flask_testing import TestCase
import run

class TestFlaskBase(TestCase):
    def create_app(self):
        self.app = run.app
        return run.app

    def setUp(self):
        self.client = self.app.test_client()
        self.client.testing = True
