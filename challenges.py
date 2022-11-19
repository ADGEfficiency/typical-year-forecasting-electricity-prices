import pathlib

import pandas as pd

data = pd.read_parquet("./data/tmy-forecast.parquet")
subset = data.loc[
    "2052-01-31T23:50:00":"2052-02-01T00:05:00",
    [
        "original-timestamps",
        "price",
    ],
]
subset["day-of-week"] = subset["original-timestamps"].dt.day_of_week
print(subset)

table = pathlib.Path("./tables/table5.md")
print(f"writing to {table}")
table.write_text(subset.reset_index().to_markdown(index=False))
