## UNIT TESTS
import itertools as it
import random

from algorithmx import *


def test_algorithmx(
    X: CommunicationStructure,
    source: int,
    sink: int = None,
    debug: bool = False,
    verbose: int = False,
):
    path = algorithm_x(source, sink, X, debug=debug, verbose=max(0, verbose - 1))
    ok = "TRUE" if path[0] == source and path[-1] == sink else "FALSE"
    loop_free = "TRUE" if len(path) == len(set(path)) else "FALSE"
    if verbose:
        print(f"{path}: {ok}")
        print(f"loop_free({path}): {loop_free}")
        print("-" * 40)
    return (source, sink), X, path, loop_free, ok


# Print test report: optional
def print_report(test_report: list):
    print(f"Test report:")
    print("(s, t), X_d, #nodes, path, loop_free, t_reached")
    print("-" * 55)
    [print(*test_instance) for test_instance in test_report]


debug = False
print("#" * 40)
dim_range = range(2, 11)
report = []
for d in dim_range:
    X = CommunicationStructure(d)

    sources = set([0, 1])
    sinks = set([X.num_nodes - 1])
    if d > 1:
        sources.update([2])
        sinks.update([2])
    if d > 2:
        sources.update([4])
        sinks.update([5, 6])
    if d > 3:
        sources.update([random.randrange(3, X.num_nodes - 1)] * int(d))
    for source, sink in it.product(sources, sinks):
        res = test_algorithmx(X, source, sink, debug=debug, verbose=0)
        report += [res]

print("#" * 40)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1] == "TRUE"])
num_loopfree = len([1 for test in report if test[-2] == "TRUE"])
print(f"Tests passed: {num_passed}/{num_tests}")
print(f"Loop free paths: {num_loopfree}/{num_tests}")


# print_report(report)
