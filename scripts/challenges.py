"""produces the table to show misalignment on day of week"""
import pathlib

import pandas as pd

if __name__ == "__main__":
    data = pd.read_parquet("./data/tmy-forecast.parquet")
    subset = data.loc[
        "2052-01-31T23:50:00":"2052-02-01T00:05:00",
        [
            "original-timestamps",
            "price",
        ],
    ]
    subset["day-of-week-forecast"] = subset.index.day_of_week
    subset["day-of-week-original"] = subset["original-timestamps"].dt.day_of_week
    table = pathlib.Path("./tables/table5.md")
    print(f"writing to {table}")
    table.write_text(subset.reset_index().to_markdown(index=False))
