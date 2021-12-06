# %%
from typing import Tuple


def get_depth(bits_lsbfirst: int, d)-> int:
    """finds the index of the first zero bit"""
    ls_ones = bits_lsbfirst.split("0")[0]
    return d - len(ls_ones)


def get_parent(i: int, d: int) -> int:
    root:int = (1 << d - 1) - 1
    if i == root:
        return None

    # essentially: get binary sequence with idx=0 being the LSB
    bits:str = bin(i)[2:].zfill(d)[::-1]
    level_i:int = get_depth(bits, d)

    difference_to_parent:int =  1 << (d - level_i)

    # The idea is similar to above:
    # We know that the parent must be bigger or smaller by exactly 'difference_to_parent'
    # So we simply test the first candidate.
    candidate:int = i - difference_to_parent

    bits_candidate:str = bin(candidate)[2:].zfill(d)
    level_candidate:int = get_depth(bits_candidate[::-1], d)

    # If level(candidate) == level_i + 1
    if candidate > 0 and level_candidate == level_i - 1:
        return candidate
    # else it's the other possibility
    return i + difference_to_parent


def get_children(i: int, d: int)-> Tuple[int,int]:
    # cut of the leading '0b' then left pad to bit_length of tree with '0's and invert the sequence
    # essentially: get binary sequence with idx=0 being the LSB
    bits = bin(i)[2:].zfill(d)[::-1]

    # check if leaf
    if bits[0] == "0": 
        return None, None

    level_i = get_depth(bits, d)
    offset_to_children = 1 << (d - 1 - level_i)

    return (i - offset_to_children, i + offset_to_children)


d = 5
i = 16
print(f"i: {i}")
print(f"children: {get_children(i, d)}")
print(f"parent : {get_parent(i, d)}")
# %% Unit tests 1
# d = 4
d = 4
p = 2 << d - 1
print(f"p = {p}, d = {d}")
print("Test parents")
report = []
for i, par in [
    (7, None), 
    (3, 7), 
    (11, 7),
    (1, 3), 
    (5, 3),
    (9, 11),
    (13, 11)
    ]:

    out = get_parent(i, d)
    result = (i, (out, par), out == par)
    report += [result]
    print(result)
    

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

# %% Unit tests 2

# d = 5
d = 5
p = 2 << d - 1
print(f"p = {p}, d = {d}")
print("Test parents")
report = []
for i, par in [
    # left
    (7, 15), 

    (3, 7), 
    (11, 7), 
    
    (1, 3), 
    (5, 3),
    (9, 11),
    (13, 11),

    (0, 1), 
    (2, 1),
    (4, 5),
    (6, 5),
    (8, 9), 
    (10, 9),
    (12, 13),
    (14, 13),

    # root
    (15, None), 

    # right
    (23, 15), 

    (19, 23), 
    (27, 23), 

    (17, 19), 
    (21, 19),
    (25, 27), 
    (29, 27),

    (16, 17), 
    (18, 17), 
    (20, 21), 
    (22, 21), 
    (24, 25), 
    (26, 25), 
    (28, 29), 
    (30, 29), 

    ]:

    out = get_parent(i, d)
    result = (i, (out, par), out == par)
    report += [result]
    if result[-1] == False:
        print(result)
    # else:
    #     print("-")

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")
# %%

print(f"p = {p}, d = {d}")
print("Test children")
report = []
for i, lchild, rchild in [
    # left
    (0, None, None),
    (2, None, None),
    (4, None, None),
    (6, None, None),
    (8, None, None),
    (10, None, None),
    (12, None, None),
    (14, None, None),

    (1, 0, 2),
    (5, 4, 6),
    (9, 8, 10),
    (13, 12, 14),

    (3, 1, 5),
    (11, 9, 13),

    (7, 3, 11),

    # root
    (15, 7, 23),

    # right
    (16, None, None),
    (18, None, None),
    (20, None, None),
    (22, None, None),
    (24, None, None),
    (26, None, None),
    (28, None, None),
    (30, None, None),

    (17, 16, 18),
    (21, 20, 22),
    (25, 24, 26),
    (29, 28, 30),

    (19, 17, 21),
    (27, 25, 29),

    (23, 19, 27),
]:
    children_true = (lchild, rchild)
    out = get_children(i, d)
    if out == None:
        out = (None, None)
    result = (i, (out, children_true), out == children_true)
    report += [result]

    if result[-1] == False:
        print(result)
    # else:
    #     print("-")

print("#" * 30)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1]])
print(f"Tests passed: {num_passed}/{num_tests}")

# %%
