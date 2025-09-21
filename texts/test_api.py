# tests/test_api.py
import json
import threading
import time
import unittest
import socket
import requests

from http.server import HTTPServer
from api import Handler, APP_NAME

def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    addr, port = s.getsockname()
    s.close()
    return port

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = _free_port()
        cls.host = "127.0.0.1"
        cls.server = HTTPServer((cls.host, cls.port), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def url(self, path):
        return f"http://{self.host}:{self.port}{path}"

    def test_index(self):
        r = requests.get(self.url("/"))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["name"], APP_NAME)

    def test_solve(self):
        r = requests.get(self.url("/solve?nums=4,7,8,8"))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("solutions", data)
        self.assertGreaterEqual(data["count"], 0)

    def test_check(self):
        # 先拿一个解
        r = requests.get(self.url("/solve?nums=4,7,8,8"))
        sols = r.json()["solutions"]
        payload = {"expr": sols[0] if sols else "(4+7+8+8)", "nums": [4,7,8,8]}
        r2 = requests.post(self.url("/check"), json=payload)
        self.assertEqual(r2.status_code, 200)
        data = r2.json()
        self.assertIn("valid", data)

    def test_404(self):
        r = requests.get(self.url("/not-found"))
        self.assertEqual(r.status_code, 404)

if __name__ == "__main__":
    unittest.main()
