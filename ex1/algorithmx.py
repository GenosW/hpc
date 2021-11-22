# %%
import functools
import math

class CommunicationStructure:
  name:str = "Shuffle-Exchange"
  def __init__(self, d):
    self.d = d
    self.num_nodes = 2 ** d

  def __repr__(self) -> str:
      return f"X_{self.d}, #nodes = {self.num_nodes}"

  def __str__(self) -> str:
      return self.__repr__()

def binary_filled(i:int, num_bits:int=8) -> str:
  return bin(i).split("b")[1].zfill(num_bits)

def bxor(x:int, y:int) -> str:
  """bitwise xor with debugging output"""
  x_bin, y_bin = bin(x), bin(y)
  print(x_bin, y_bin)
  return x ^ y

def shuffle(bits:str) -> int:
  shuffled = bits[1:] + bits[0]
  dec = int(shuffled, base=2)
  return dec

def algorithm_x(i:int, j:int, X:CommunicationStructure, debug:bool=False, verbose:bool=True):
  if verbose:
    print(f"Computing path from i={i} -> j={j} in X_{X.d}")
  if i == j:
    return [i]


  d:int = X.d
  u:int = i
  e:int = d-1

  path:list = [u] # start at node u = i

  # function used to generate bit sequences of a fixed length
  binary = functools.partial(binary_filled, num_bits=X.d)
  j_bits_r:str = binary(j)[::-1] # reversing the order so it's b0 b1 b2 ... --> easier to work with

  while(e >= 0):
    u_bits:str = binary(u)
    # X2: b
    b:str = u_bits[-1]
    if debug:
      print(f"X2: b = {b}")

    # X3: Exchange
    if debug:
      print("X3: Exchange")
    b_prime_e:str = j_bits_r[e]
    if cmp := b != b_prime_e:
      v:int = u ^ 1 if not debug else bxor(u, 1) 
      path += [v]
      if verbose:
        print(f"{u} -> {v}")
      u = v
      if u == j:
        return path

    # X4: Shuffle
    if debug:
      print("X4: Shuffle")
    v = shuffle(binary(u))
    if v != u:
      path += [v]
      if verbose:
        print(f"{u} -> {v}")
      u = v
    # X5: 
      if u == j:
        return path

    e -= 1
  return path
    

if __name__ == "__main__":
  # A simple example
  X = CommunicationStructure(3)
  path = algorithm_x(2, 7, X, debug=True)
  print(f"Path: {path}")
