# cli.py
# 简单命令行：传入四个整数，打印全部解法

import sys
from game24 import solve

def main(argv):
    if len(argv) != 4:
        print("用法: python cli.py a b c d")
        return 1
    try:
        nums = [int(x) for x in argv]
    except ValueError:
        print("错误: 需要 4 个整数")
        return 1
    sols = solve(nums)
    if not sols:
        print("无解")
    else:
        print(f"共 {len(sols)} 个解：")
        for s in sols:
            print(s)
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
