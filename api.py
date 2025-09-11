# api.py
# 纯 Python REST API（BaseHTTPRequestHandler），提供 24 点求解与校验

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import threading
from typing import Any, Dict, Tuple

import sys
sys.setrecursionlimit(10000)

from game24 import solve, check_expression

APP_NAME = "Game24 REST API"
APP_VERSION = "1.0.0"
DEFAULT_HOST = os.environ.get("GAME24_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("GAME24_PORT", "5000"))

def json_response(handler: BaseHTTPRequestHandler, status: int, payload: Dict[str, Any]):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)

def parse_nums(value: str) -> Tuple[bool, Any]:
    try:
        parts = [p.strip() for p in value.split(",")]
        nums = [int(x) for x in parts if x]
        if len(nums) != 4:
            return False, "nums 必须是 4 个整数，例如 nums=4,7,8,8"
        return True, nums
    except Exception:
        return False, "nums 解析失败，示例：nums=4,7,8,8"

class Handler(BaseHTTPRequestHandler):
    server_version = f"{APP_NAME}/{APP_VERSION}"

    def _send_error(self, status: int, code: str, message: str, details: Dict[str, Any] = None):
        json_response(self, status, {
            "error": {"code": code, "message": message, "details": details or {}}
        })

    def do_OPTIONS(self):
        # CORS 预检
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept, User-Agent")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            return json_response(self, 200, {
                "name": APP_NAME,
                "version": APP_VERSION,
                "endpoints": {
                    "health": "GET /healthz",
                    "solve": "GET /solve?nums=1,2,3,4",
                    "check": "POST /check {expr, nums}",
                }
            })

        if path == "/healthz":
            return json_response(self, 200, {"status": "ok"})

        if path == "/solve":
            nums_q = qs.get("nums", [])
            if not nums_q:
                return self._send_error(400, "INVALID_QUERY", "缺少查询参数 nums，例如 /solve?nums=4,7,8,8")
            ok, res = parse_nums(nums_q[0])
            if not ok:
                return self._send_error(400, "INVALID_NUMS", str(res))
            try:
                sols = solve(res)
                return json_response(self, 200, {"count": len(sols), "solutions": sols})
            except Exception as e:
                return self._send_error(500, "SOLVE_ERROR", "求解失败", {"exception": str(e)})

        # 未知路径
        return self._send_error(404, "NOT_FOUND", f"路径不存在: {path}")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/check":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length) if length > 0 else b"{}"
                data = json.loads(raw.decode("utf-8"))
            except Exception:
                return self._send_error(400, "INVALID_JSON", "请求体不是合法 JSON")

            expr = data.get("expr")
            nums = data.get("nums")
            if not isinstance(expr, str) or not isinstance(nums, list):
                return self._send_error(400, "INVALID_BODY", "需要字段 expr(string) 与 nums(array[int])")

            if len(nums) != 4 or not all(isinstance(x, int) for x in nums):
                return self._send_error(400, "INVALID_NUMS", "nums 必须为 4 个整数")

            try:
                ok = check_expression(expr, nums)
                return json_response(self, 200, {"valid": ok})
            except Exception as e:
                return self._send_error(500, "CHECK_ERROR", "校验失败", {"exception": str(e)})

        return self._send_error(404, "NOT_FOUND", f"路径不存在: {path}")

def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    server = HTTPServer((host, port), Handler)
    print(f"{APP_NAME} listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    run()
