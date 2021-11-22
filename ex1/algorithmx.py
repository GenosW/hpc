# %%
import math

class CommunicationStructure:
  name:str = "Shuffle-exchange"
  def __init__(self, d):
    self.d = d
    self.num_nodes = 2 ** d
    self.num_bits = int(math.log2(self.num_nodes))
    print(f"X_{d}, #nodes = {self.num_nodes}, #bits = {self.num_bits}")

def algorithm_x(i:int, j:int, X:CommunicationStructure, debug:bool=False):

  def binary(i:int) -> str:
    return bin(i).split("b")[1].zfill(X.num_bits)

  def bxor(x:int, y:int) -> str:
    x_bin, y_bin = bin(x), bin(y)
    # print(x_bin)
    # print(y_bin)
    return int(x_bin, base=2) ^ int(y_bin, base=2) # ^... bitwise xor operator

  def shuffle(bits:str):
    # print(f"shuffling bits: {bits}", end="")
    shuffled = bits[1:] + bits[0]
    dec = int(shuffled, base=2)
    # print(f" --> {shuffled} (dec={dec})")
    return dec

  print(f"Computing path from i={i} -> j={j} in X_{X.d}")

  d:int = X.d
  u:int = i
  e:int = d-1 # start at node u

  path:list = [u]

  j_bits:str = binary(j)
  j_bits_r = j_bits[::-1]

  counter = 10
  while(e >= 0 and counter > 0):
    u_bits:str = binary(u) #[::-1]
    # X2: b
    if debug:
      print("X2: b")
    b:str = u_bits[-1]

    # X3: Exchange
    if debug:
      print("X3: Exchange")
    b_prime_e:str = j_bits_r[e]
    if cmp := b != b_prime_e:
      v:int = u ^ 1 if not debug else bxor(u, 1) 
      path += [v]
      if debug:
        print(f"{u} -> {v}")
      u = v # now at node u
      if u == j:
        return path
    else:
      v = u

    # X4: Shuffle
    if debug:
      print("X4: Shuffle")
    v_bits = shuffle(binary(v))
    # print(f"v_bits = {v_bits}")
    v = int(v_bits)
    if v != u:
      path += [v]
      if debug:
        print(f"{u} -> {v}")
      u = v
      e -= 1

    # X5: 
    if debug:
      print("X5:")
    if u == j:
      return path

    counter -= 1
    if debug:
      print("Algorithm spun out")
  return path
    
def test_algorithmx(d:int, source:int, sink:int=None, debug:bool=False):
  X = CommunicationStructure(d)
  sink = sink or X.num_nodes - 1
  path = algorithm_x(source, sink, X, debug=debug)
  ok = "OK" if path[0] == source and path[-1] == sink else "FAIL"
  print(f"{path}: {ok}")
  return (source, sink), path, ok

# %%
import itertools as it

debug = False
print("#"*40)
report = []
for i in range(2,4):
  for source, sink in it.product([0,1,2], [1, 3, None]):
    res = test_algorithmx(i, source, sink, debug=debug)
    report += [res]
  print("-"*40)
print("#"*40)

# %%
report
# %%

# %%
X = CommunicationStructure(3)
algorithm_x(1, 2, X, debug=False)