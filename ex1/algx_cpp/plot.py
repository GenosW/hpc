# %%
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# %%
script_dir = pathlib.Path(__file__).parent
print(f"Looking for csv-files in {script_dir}")
found_files = list(script_dir.glob("*.csv"))
print(f"Found files: {found_files}")

joined = []
joined_norm = []
averages = {"5": 0, "10" : 0, "15": 0}
names = []
past_last_nonzero_idx = None
for file in found_files:
    name = file.name.split(".")[0].split("_")[-1]
    names.append(name)
    arr = np.fromfile(file, sep=",", dtype="int64")
    average = np.sum([i*val for i, val in enumerate(arr)])
    tmp = pd.Series(arr)
    total_paths = arr.sum()
    joined.append(tmp)
    joined_norm.append(tmp / total_paths)
    averages[name] = average / total_paths

    if "15" in file.name:
        for idx, e in enumerate(arr[::-1]):
            if e != 0:
                index = idx
                break
        past_last_nonzero_idx = len(arr) - index


def join_series(liste):
    if past_last_nonzero_idx != None:
        return (
            pd.concat(liste, join="outer", axis=1)
            .iloc[:past_last_nonzero_idx, :]
            .fillna(0)
        )
    return pd.concat(liste, join="outer", axis=1).fillna(0)

order = ["5", "10", "15"]

joined = join_series(joined).convert_dtypes(convert_integer=True)
joined_norm = join_series(joined_norm)

# Name columns and reorder
joined.columns = names
joined_norm.columns = names
joined = joined[order]
joined_norm = joined_norm[order]

# %%
# Plot data
fig, axs = plt.subplots(2, figsize=(12, 10))
joined_norm[["5", "10", "15"]].plot(kind="bar", ax=axs[0], width=2)
joined_norm[["5", "10", "15"]].plot(kind="kde", ax=axs[1], lw=2)

for d, color in zip(averages, ["tab:blue", "tab:orange", "tab:green"]):
    axs[0].axvline(averages[d], linestyle="--", color=color, label=f"mean[{d}]: {averages[d]:.1f}")

# Make plots prettier
for ax in axs:
    ax.grid(True)
    ax.legend(title="d")

axs[0].set_ylabel("Frequency")

fig.suptitle(
    "Relative Frequency Histogram of lengths of paths\ncomputed via 'Algorithm X' for different $\it{X}_d$",
    fontsize=24,
    usetex=True,
)

axs[1].set_title("Kernel Density Estimation (KDE) Plot", fontsize=18, usetex=True)

png = script_dir / "ex1_histogram_pathlengths.png"
svg = script_dir / "ex1_histogram_pathlengths.svg"
print("Saving figures:")
print(f"- {png}")
print(f"- {svg}")
plt.savefig(png, bbox_inches="tight", pad_inches=0.1)
plt.savefig(svg, bbox_inches="tight", pad_inches=0.1)

