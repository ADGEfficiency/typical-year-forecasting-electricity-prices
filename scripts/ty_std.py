import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ty.cli import cli
from ty.data import load_prices
from ty.forecast import typical
from ty.util import get_plot_base


def typical_month_mean_std(data: pd.DataFrame, month: int) -> pd.DataFrame:
    means = typical(data, "mean", month)
    stds = typical(data, "std", month)
    ds = means.merge(stds)
    ds["error"] = ds["error-mean"] + ds["error-std"]
    return ds


if __name__ == "__main__":
    args = cli()
    base = get_plot_base(args.plot_mode)
    data = load_prices()
    data = data.rename({"RRP": "price"}, axis=1)
    sns.set_context(rc={"font.size": 14, "axes.titlesize": 14, "axes.labelsize": 14})

    """
    just do all years at once

    make the table

    then plot the two forecasts on top of each other
    """

    samples = []
    forecasts = []
    months = data.index.month.unique().sort_values()
    for month in months:
        errors = typical_month_mean_std(data, month)
        sample = errors.iloc[np.argmin(errors["error"]), :]
        samples.append(sample)

        forecast = data.loc[
            (data.index.year == sample.year)
            & (data.index.month == sample["month-int"]),
            :,
        ]
        forecast.index = forecast.index.map(lambda x: x.replace(year=2052))
        forecasts.append(forecast)

    samples = pd.concat(samples, axis=1).T
    samples = samples[
        [
            "month",
            "year",
            "price-mean",
            "long-term-mean",
            "price-std",
            "long-term-std",
            "error",
        ]
    ]
    table = pathlib.Path("./tables/table4.md")
    print(f"writing to {table}")
    table.write_text(samples.to_markdown(index=False))

    """
    let's grab the interval data and plot
    """

    forecasts = pd.concat(forecasts, axis=0)
    f, ax = plt.subplots(
        figsize=(12, 0.8 * 1.5 * 4.8), nrows=2, sharex=True, sharey=True
    )
    ax = ax.flatten()
    forecast_mean = pd.read_parquet("./data/tmy-forecast.parquet")
    ax[0].set_title("Mean Only")
    sns.lineplot(
        forecast_mean.reset_index(),
        ax=ax[0],
        y="price",
        x="interval-start",
        color="deepskyblue",
    )
    sns.lineplot(
        forecasts.reset_index(),
        ax=ax[1],
        y="price",
        x="interval-start",
        color="darkorchid",
    )
    ax[1].set_title("Mean & Standard Deviation")
    plt.tight_layout()
    out = base / "f4.png"
    print(f"plot to {out}")
    f.savefig(out)
