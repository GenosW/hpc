# %%
from typing import Tuple


def get_family(i: int, d: int) -> Tuple[int, int, int]:
    difference_to_left:int = 1 << (d - 1)
    root_value:int = (1 << d ) - 2
    split_value:int = root_value >> 1

    depth_i:int = 0
    parent:int = None # returns parent = None if i == root
    while(i != root_value and depth_i != d):
        parent = root_value

        if i < split_value: # left subtree
            root_value = root_value - difference_to_left
        else: # left subtree
            root_value = root_value - 1

        # Compute values for next level
        # bitshift instead of division by 2
        difference_to_left = difference_to_left >> 1 # 'cache' for reuse
        split_value = root_value - difference_to_left + 1
        depth_i += 1

    # 'if is not Leaf'
    if depth_i < d - 1: 
        return parent, i - difference_to_left, i-1

    # returns children = (None, None) if i is leaf
    return parent, None, None


# %% Simple test
d = 4
p = (1 << d) - 1
i = 1
family = get_family(i, d)
print("-"*30)
print(f"i: {i}")
print(f"parent: {family[0]}")
print(f"children: {family[1:]}")
# %% Unit test 1
# Complete, balanced binary tree with depth 4
d = 4
p = (1 << d) - 1
print(f"p = {p}, d = {d}")
report = []
for i, par, lchild, rchild in [
    (0, 2, None, None),
    (1, 2, None, None),
    (3, 5, None, None),
    (4, 5, None, None),
    (7, 9, None, None),
    (8, 9, None, None),
    (10, 12, None, None),
    (11, 12, None, None),
    (2, 6, 0, 1),
    (5, 6, 3, 4),
    (9, 13, 7, 8),
    (12, 13, 10, 11),
    (6, 14, 2, 5),
    (13, 14, 9, 12)
    ]:
    out = get_family(i, d)
    result = (
        i, 
        (out[0], par, par_correct := out[0] == par), 
        (out[1], lchild, lchild_correct := out[1] == lchild), 
        (out[2], rchild, rchild_correct := out[2] == rchild),
        par_correct and lchild_correct and rchild_correct
    )
    report += [result]
    print(result)

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")
# %% Unit test 2
# Complete, balanced binary tree with depth 5
d = 5
p = (1 << d) - 1
print(f"p = {p}, d = {d}")
report = []
for i, par, lchild, rchild in [
    # left tree
    (0, 2, None, None),
    (1, 2, None, None),
    (3, 5, None, None),
    (4, 5, None, None),
    (7, 9, None, None),
    (8, 9, None, None),
    (10, 12, None, None),
    (11, 12, None, None),
    (2, 6, 0, 1),
    (5, 6, 3, 4),
    (9, 13, 7, 8),
    (12, 13, 10, 11),
    (6, 14, 2, 5),
    (13, 14, 9, 12),
    (14, 30, 6, 13),

    # root
    (30, None, 14, 29),

    # right tree
    (15, 17, None, None),
    (16, 17, None, None),
    (18, 20, None, None),
    (19, 20, None, None),
    (22, 24, None, None),
    (23, 24, None, None),
    (25, 27, None, None),
    (26, 27, None, None),

    (17, 21, 15, 16),
    (20, 21, 18, 19),

    (24, 28, 22, 23),
    (27, 28, 25, 26),

    (21, 29, 17, 20),
    (28, 29, 24, 27),

    (29, 30, 21, 28),
    ]:
    out = get_family(i, d)
    result = (
        i, 
        (out[0], par, par_correct := out[0] == par), 
        (out[1], lchild, lchild_correct := out[1] == lchild), 
        (out[2], rchild, rchild_correct := out[2] == rchild),
        par_correct and lchild_correct and rchild_correct
    )
    report += [result]
    # print(result)

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")
# %%
