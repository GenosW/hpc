import pandas as pd
import pathlib


script_dir = pathlib.Path(__file__).parent
print(script_dir)

data = pd.read_csv(script_dir / "lengths.csv")

binned = []
binned_norm = []
for d in ["3", "5", "10", "15"]:
    tmp = data[d].dropna().convert_dtypes(convert_integer=True)
    tmp = tmp.value_counts().sort_index()
    binned += [tmp]
    binned_norm += [tmp / tmp.sum()]  # normalized
    # binned_norm += [tmp.value_counts(normalize=True).sort_index()]
joined = pd.concat(binned, axis=1).rename_axis("path_length")
joined_norm = pd.concat(binned_norm, axis=1).rename_axis("path_length")

joined.to_csv(script_dir / "lengths_binned.csv")
joined_norm.to_csv(script_dir / "lengths_norm_binned.csv")
