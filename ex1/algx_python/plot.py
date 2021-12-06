# %%
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
script_dir = pathlib.Path(__file__).parent
print(script_dir)

joined = pd.read_csv(script_dir / "lengths_binned.csv", index_col="path_length")
joined_norm = pd.read_csv(
    script_dir / "lengths_norm_binned.csv", index_col="path_length"
)
joined_norm.describe()
# %%
fig, axs = plt.subplots(2, figsize=(10, 10))
joined_norm.plot(kind="bar", ax=axs[0])
joined_norm.plot(kind="kde", ax=axs[1])
