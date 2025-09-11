# game24.py
# 24点求解器：给定四个整数，找出用 + - * / 与括号得到 24 的表达式（每个数恰用一次）

from fractions import Fraction
from typing import List, Tuple, Iterable, Set

OPS = [
    ("+", lambda a, b: a + b),
    ("-", lambda a, b: a - b),
    ("*", lambda a, b: a * b),
    ("/", lambda a, b: a / b if b != 0 else None),
]

def _pair_combine(vals: List[Tuple[Fraction, str]]) -> Iterable[Tuple[List[Tuple[Fraction, str]], None]]:
    """从当前值列表中选择两个做运算，并生成新的值列表"""
    n = len(vals)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = vals[i], vals[j]
            rest = [vals[k] for k in range(n) if k not in (i, j)]
            yield a, b, rest

def solve(nums: List[int], target: int = 24) -> List[str]:
    """返回所有可行表达式（字符串形式），若无解则空列表"""
    if len(nums) != 4:
        raise ValueError("nums 必须是 4 个整数")
    vals = [(Fraction(n), str(n)) for n in nums]
    target_frac = Fraction(target, 1)
    seen: Set[str] = set()
    results: Set[str] = set()

    def dfs(items: List[Tuple[Fraction, str]]):
        if len(items) == 1:
            val, expr = items[0]
            if val == target_frac:
                # 归一化表达式以去重
                key = expr.replace(" ", "")
                if key not in seen:
                    seen.add(key)
                    results.add(expr)
            return

        # 选两两组合运算
        for a, b, rest in _pair_combine(items):
            av, ae = a
            bv, be = b
            for op, fn in OPS:
                # 为了避免等价表达式重复：对 +、* 交换律做简单剪枝
                if op in {"+", "*"}:
                    if ae > be:  # 以字典序固定顺序
                        continue
                if op == "/" and bv == 0:
                    continue
                out = fn(av, bv)
                if out is None:
                    continue
                new_expr = f"({ae} {op} {be})"
                dfs(rest + [(out, new_expr)])

    dfs(vals)
    # 结果美化：去掉最外层多余括号
    pretty = []
    for e in results:
        if e.startswith("(") and e.endswith(")"):
            # 简单剥一层
            e2 = e[1:-1]
            pretty.append(e2)
        else:
            pretty.append(e)
    # 排序稳定输出
    return sorted(set(pretty))

def check_expression(expr: str, nums: List[int], target: int = 24) -> bool:
    """校验表达式是否只使用了给定四个数且结果为 target"""
    # 简单方式：尝试求解所有合法表达式，判断 expr 是否在其中（稳妥但可能较慢）
    sols = solve(nums, target=target)
    norm = expr.replace(" ", "")
    return any(s.replace(" ", "") == norm for s in sols)

if __name__ == "__main__":
    print(solve([4,7,8,8]))
