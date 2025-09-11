# tests/test_game24.py
import unittest
from game24 import solve, check_expression

class TestGame24(unittest.TestCase):
    def test_basic(self):
        sols = solve([4,7,8,8])
        self.assertTrue(any(eval(s) == 24 for s in sols))

    def test_no_solution_example(self):
        # 并非所有四元组都有解，给一个常见无解组合（可能随实现变动）
        sols = solve([1,1,1,1])
        self.assertEqual(len(sols), 0)

    def test_check_expression_true(self):
        nums = [4,7,8,8]
        # (8 - 7) * (8 + 4) = 1 * 12 = 12  —— 这不是 24，换一个
        # (8 / (7 - 4)) * 8 = (8/3)*8 = 64/3 != 24，也不行
        # 用一个可行的（示例可能依实现不同，你可以替换为解集中一个）
        sols = solve(nums)
        self.assertTrue(len(sols) > 0)
        self.assertTrue(check_expression(sols[0], nums))

    def test_check_expression_false(self):
        nums = [4,7,8,8]
        self.assertFalse(check_expression("(4+7+8+8)", nums))

if __name__ == "__main__":
    unittest.main()
