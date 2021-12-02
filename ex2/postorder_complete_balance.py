# %%
import math

# %%
def binary(i: int) -> str:
    return bin(i).split("b")[1]


def child_left(i: int) -> int:
    if i % 2:
        return i ^ 1
    return int((i - 1) / 2)  # it's a leaf


def depth(p):
    return int(math.log2(p + 1))


def parent(i: int, p: int):
    root = int(p / 2 - 1)
    if i == root:
        return i
    levels = p.bit_length() - 1
    bits = bin(i)[2:].zfill(
        levels
    )  # cut of the leading '0b' then left pad to bit_length of tree with '0's

    # reverse-ordered search for first '0'
    # e.g. 13 ^= 1101 = b3 b2 b1 b0
    # target for above example is b1
    # --> idx_r = 1 <=> idx = 2
    idx_r = bits[::-1].index("0")
    idx = len(bits) - idx_r - 1

    if bits[idx - 1] == "1":
        return int(bits, base=2) ^ (2 << (idx_r - 1)) ^ (2 << (idx_r))
    return int(bits, base=2) ^ (2 << (idx_r - 1))


# %%
d = 4
p = 2 << d - 1
print(f"p = {p}, d = {d}")
i = 5
print(f"i={i} : {parent(i, p)}")
# %%
print(f"p = {p}, d = {d}")
print("Test parents")
report = []
for i, par, _ in [(1, 3, 0), (3, 7, 1), (5, 3, 4), (7, 7, 3), (13, 11, 12)]:
    # , lchild, rchild
    out = parent(i, p)
    result = (i, (out, par), out == par)
    report += [result]
    print(result)
    # report += [child_left(i) == correct]

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")
# %%
print(f"p = {p}, d = {d}")
print("Test children")
report = []
for i, lchild, rchild in [(2, 0, 1)]:
    children_true = (lchild, rchild)
    out = children(i, p)
    result = (i, (out, children_true), out == children_true)
    report += [result]
    print(result)

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")

# %%

# %%
