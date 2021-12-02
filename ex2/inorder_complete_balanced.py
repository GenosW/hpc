# %%
import math

# %%
def binary(i: int) -> str:
    return bin(i).split("b")[1]

def get_parent(i: int, d:int):
    # root = int(p / 2 - 1)
    root = (1 << d-1) - 1
    if i == root:
        return i
    levels = d #p.bit_length() - 1
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
def is_leaf(bits:int):
    return True if bits[-1] == "0" else False

def get_depth(bits_lsbfirst:int, d):
    ls_ones = bits_lsbfirst.split("0")[0]
    # print(f"ls_ones: {ls_ones}")
    return d - 1 - len(ls_ones)

def get_children(i:int, d:int):
    levels = d #p.bit_length() - 1

    bits = bin(i)[2:].zfill(
        levels
    )  # cut of the leading '0b' then left pad to bit_length of tree with '0's
    if is_leaf(bits):
        return None

    level_i = get_depth(bits[::-1], d)
    offset_to_children = 1 << (d - 2 - level_i)
    
    return (i-offset_to_children, i+offset_to_children)
# %%
d = 4
i = 13
children = get_children(i, d)
print(f"i: {i}")
print(f"children: {children}")
# %%
d = 4
p = 2 << d - 1
print(f"p = {p}, d = {d}")
i = 5
print(f"i={i} : {get_parent(i, p, d)}")
print(f"i={i} : {children(i, p, d)}")
j = 0
print(f"i={j} : {children(j, p, d)}")
# %%
print(f"p = {p}, d = {d}")
report = []
for i, par, _ in [(1, 3, 0), (3, 7, 1), (5, 3, 4), (7, 7, 3), (13, 11, 12)]:
    # , lchild, rchild
    out = get_parent(i, d)
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
for i, lchild, rchild in [
    (0, None, None),
    (2, None, None),
    (4, None, None),
    (6, None, None),
    (8, None, None),
    (10, None, None),
    (12, None, None),
    (14, None, None),
    (1, 0, 2),
    (3, 1, 5),
    (5, 4, 6),
    (7, 3, 11),
    (11, 9, 13),
    (9, 8, 10),
    (13, 12, 14),
    ]:
    children_true = (lchild, rchild)
    out = get_children(i, d)
    if out == None:
        out = (None, None)
    result = (i, (out, children_true), out == children_true)
    report += [result]
    print(result)

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")

# %%

# %%
