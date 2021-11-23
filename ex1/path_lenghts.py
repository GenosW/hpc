import itertools as it
import pathlib

import pandas as pd

from algorithmx import *

results = {}
for d in [3, 5, 10, 15]:
    X = CommunicationStructure(d)
    lengths = []
    for i, j in it.combinations(range(X.num_nodes), 2):
        path = algorithm_x(i, j, X, verbose=False)
        lengths += [len(path) - 1]
    results[d] = lengths

df = []
for d in results:
    df += [pd.DataFrame(results[d], columns=[d])]
df = pd.concat(df, axis=1)

print(df.info())
print(df.describe())

script_dir = pathlib.Path(__file__).parent
print(script_dir)
df.to_csv(script_dir / "lengths.csv")
