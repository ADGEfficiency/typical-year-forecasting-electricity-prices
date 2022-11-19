import pathlib

import pandas as pd
from nemdata.loader import loader


def load_prices():
    """load price data - either from a local Parquet file or from nemdata cache"""
    cache = pathlib.Path("./data/trading-price.parquet")
    cache.parent.mkdir(exist_ok=True, parents=True)

    if cache.exists():
        print(f"loading from {cache}")
        return pd.read_parquet(cache)

    print(f"loading from nemdata")
    data = loader("trading-price")["trading-price"]
    data = data.set_index("interval-start")

    region = "SA1"
    mask = data["REGIONID"] == region
    data = data[mask]

    dt = data.index
    d_min = dt.min()
    d_max = dt.max()
    print(f"loaded price data from {d_min} to {d_max}")
    data = data.loc[:, "RRP"].to_frame()

    data.to_parquet(cache)
    return data.sort_index()


if __name__ == "__main__":
    load_prices()
