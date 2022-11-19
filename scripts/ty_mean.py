"""create typical year forecast using the mean as the statistic"""
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ty.cli import cli
from ty.data import load_prices
from ty.forecast import typical
from ty.util import get_plot_base

if __name__ == "__main__":
    args = cli()
    base = get_plot_base(args.plot_mode)
    pathlib.Path("./tables").mkdir(exist_ok=True)

    data = load_prices()
    data = data.rename({"RRP": "price"}, axis=1)
    sns.set_context(rc={"font.size": 12, "axes.titlesize": 12, "axes.labelsize": 12})

    #  January example
    jan = typical(data, "mean", 1)
    table = pathlib.Path("./tables/table2.md")
    print(f"writing to {table}")
    table.write_text(jan.drop("month-int", axis=1).to_markdown(index=False))

    #  run over all months
    samples = []
    forecasts = []
    months = data.index.month.unique().sort_values()
    for month in months:
        means = typical(data, "mean", month)
        sample = means.iloc[np.argmin(means["error-mean"]), :]
        samples.append(sample)

        forecast = data.loc[
            (data.index.year == sample.year)
            & (data.index.month == sample["month-int"]),
            :,
        ].copy()
        forecast.loc[:, "original-timestamps"] = forecast.index
        forecast.index = forecast.index.map(lambda x: x.replace(year=2052))
        forecasts.append(forecast)

    samples = pd.concat(samples, axis=1).T
    samples = samples[["month", "year", "price-mean", "long-term-mean", "error-mean"]]

    table = pathlib.Path("./tables/table3.md")
    print(f"writing to {table}")
    table.write_text(samples.to_markdown(index=False))

    #  plot forecast
    forecasts = pd.concat(forecasts, axis=0)
    forecasts.to_parquet("./data/tmy-forecast.parquet")
    f, ax = plt.subplots(figsize=(12, 0.8 * 4.8))
    sns.lineplot(
        forecasts.reset_index(),
        ax=ax,
        y="price",
        x="interval-start",
        color="deepskyblue",
    )
    plt.tight_layout()
    out = base / "f2.png"
    print(f"plot to {out}")
    f.savefig(out)

    #  plot forecast versus all years
    years = data.index.year.unique().sort_values()
    f, axes = plt.subplots(
        nrows=years.shape[0], figsize=(12, 3 * 4.8), sharex=True, sharey=True
    )
    for ax, year in zip(axes, years):
        subset = data.loc[data.index.year == year, "price"]
        subset.index = subset.index.map(lambda x: x.replace(year=2052))
        sns.lineplot(
            subset.reset_index(),
            ax=ax,
            y="price",
            x="interval-start",
            alpha=1.0,
            color="deepskyblue",
            linestyle="--",
            label="actuals",
        )
        sns.lineplot(
            forecasts.reset_index(),
            ax=ax,
            y="price",
            x="interval-start",
            alpha=0.3,
            color="gray",
            label="forecast",
        )
        ax.legend(loc="upper left")
        ax.set_title(year)

    plt.tight_layout()
    out = base / "f3.png"
    print(f"plot to {out}")
    f.savefig(out)
