## UNIT TESTS
import itertools as it

from algorithmx import *

def test_algorithmx(d:int, source:int, sink:int=None, debug:bool=False, verbose:int=False):
  X = CommunicationStructure(d)
  sink = sink or X.num_nodes - 1
  path = algorithm_x(source, sink, X, debug=debug, verbose=verbose-1)
  ok = "OK" if path[0] == source and path[-1] == sink else "FAIL"
  if verbose:
    print(f"{path}: {ok}")
  return (source, sink), X, path, ok

# Print test report: optional
def print_report(test_report:list):
  print(f"Test report:")
  print("(s, t), X_d, #nodes, path, t reached?")
  print("-"*55)
  [print(*test_instance) for test_instance in test_report]


debug = False
print("#"*40)
report = []
for d in range(2,4):
  sources = [0,1]
  sinks = [None]
  if d > 1:
    sources += [2]
    sinks += [2]
  if d > 2:
    sources += [4]
    sinks += [5, 6]

  for source, sink in it.product(sources, sinks):
    res = test_algorithmx(d, source, sink, debug=debug, verbose=1)
    report += [res]
    print("-"*40)
print("#"*40)
num_tests = len(report)
num_passed = len([1 for test in report if test[-1] == "OK"])
print(f"Tests passed: {num_passed}/{num_tests}")


# print_report(report)