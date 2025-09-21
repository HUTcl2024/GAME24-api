# api.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# 和你的仓库保持一致：solve / check_expression
from game24 import solve, check_expression

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("GAME24_PORT", "5000"))
HOST = os.environ.get("GAME24_HOST", "127.0.0.1")

def parse_nums_list(obj):
    """
    校验并转换 nums：必须是长度为 4 的数字数组
    返回 int 列表，例如 [4, 7, 8, 8]
    """
    if not isinstance(obj, list):
        raise ValueError("nums 必须是数组，例如 [4,7,8,8]")
    if len(obj) != 4:
        raise ValueError("nums 必须正好是 4 个数字")
    try:
        nums = [int(x) for x in obj]
    except Exception:
        raise ValueError("nums 必须是整数数组，例如 [4,7,8,8]")
    return nums

@app.post("/solve")
def solve_post():
    """
    官方入口：POST /solve
    body: { "nums": [4,7,8,8] }
    返回: { "nums": [...], "count": N, "solutions": [...] }
    """
    data = request.get_json(silent=True) or {}
    try:
        nums = parse_nums_list(data.get("nums"))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        # 你的求解函数：返回可迭代（list/set等）
        solutions = solve(nums)
        sols = list(solutions) if not isinstance(solutions, list) else solutions
        return jsonify({"nums": nums, "count": len(sols), "solutions": sols})
    except Exception as e:
        return jsonify({"error": f"求解失败: {e}"}), 500

@app.post("/check")
def check_post():
    """
    校验表达式是否用给定 4 数得出 24
    body: { "expr": "(8/(7-4))*8", "nums": [4,7,8,8] }
    返回: { "valid": true/false, "error": "...(可选)" }
    """
    data = request.get_json(silent=True) or {}
    expr = data.get("expr", "")
    if not expr or not isinstance(expr, str):
        return jsonify({"valid": False, "error": "缺少或非法的 expr"}), 400
    try:
        nums = parse_nums_list(data.get("nums"))
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 400

    try:
        ok = bool(check_expression(expr, nums))
        return jsonify({"valid": ok})
    except Exception as e:
        return jsonify({"valid": False, "error": f"校验失败: {e}"}), 500

if __name__ == "__main__":
    print(f"Game24 REST API listening on http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=False)
