"""creates the motivation and solution figures + tables"""
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ty.cli import cli
from ty.data import load_prices
from ty.util import get_plot_base


def project_savings(
    price: float, savings_mwh: float = 150, years: int = 4
) -> pd.DataFrame:
    """simple technical + economic model of energy project"""
    data = pd.DataFrame(
        {
            "year": list(range(years)),
            "capex": [25000, 0, 0, 0],
            "savings_mwh": [savings_mwh] * years,
            "price": [price] * years,
        }
    )
    data["savings_$"] = data["price"] * data["savings_mwh"]
    data["cumulative_savings_$"] = (data["savings_$"] - data["capex"]).cumsum()
    return data


def plot_project_savings(
    ds: pd.DataFrame, include_project_text: bool = True, include_tmy_text: bool = False
) -> plt.Figure:
    """creates figure showing project savings versus assumed prices"""
    ds = ds.sort_values("cumulative_savings_$")
    print(ds)
    f, ax = plt.subplots(figsize=[1.8 * 6.4, 0.8 * 4.8], dpi=250)

    colors = ["red" if x < 0 else "blue" for x in ds["cumulative_savings_$"].values]
    colors = ["green" if year == 2052 else c for c, year in zip(colors, ds["year"])]

    ds["x-label"] = ds.apply(lambda x: f'{x["price"]:3.2f}\n {x["year"]:4.0f}', axis=1)
    chart = sns.barplot(
        ds,
        x="x-label",
        y="cumulative_savings_$",
        ax=ax,
        palette=colors,
        label=colors,
    )

    ax.set_ylabel("Cumulative Savings $")
    ax.set_xlabel("Average Annual Price $/MWh\nYear")
    losers = list(
        sorted(ds[ds["cumulative_savings_$"] < 0]["year"].values.astype(int).tolist())
    )
    losers = ", ".join([str(l) for l in losers[:-1]]) + f" & {losers[-1]}"
    winners = list(
        sorted(ds[ds["cumulative_savings_$"] > 0]["year"].values.astype(int).tolist())
    )
    winners = ", ".join([str(l) for l in winners[:-1]]) + f" & {winners[-1]}"

    if include_project_text:
        ax.text(0.3, 20000, f"Projects in {losers} lose money", fontsize=10)
        ax.text(5, -20000, f"Projects in {winners} make money", fontsize=10)

    if include_tmy_text:
        ax.annotate(
            "Wow!",
            xy=(5.0, 3000),
            xytext=(4.4, 20000),
            arrowprops={
                "arrowstyle": "simple",
                "edgecolor": "black",
                "facecolor": "black",
            },
            va="center",
            style="italic",
            fontsize=18,
        )

    plt.tight_layout()
    return f


if __name__ == "__main__":
    sns.set_context(rc={"font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10})

    args = cli()
    base = get_plot_base(args.plot_mode)
    pathlib.Path("./tables").mkdir(exist_ok=True)

    #  table of project economics for a single year
    economics = project_savings(price=100)
    table = pathlib.Path("./tables/table0.md")
    print(f"writing to {table}")
    table.write_text(economics.to_markdown())

    #  calculate project economics for different average prices
    economics_agg = {
        "year": "mean",
        "capex": "sum",
        "savings_mwh": "sum",
        "price": "mean",
        "savings_$": "sum",
        "cumulative_savings_$": "sum",
    }
    data = load_prices()
    means = data.groupby(data.index.year)["RRP"].mean()
    projects = []
    for year, price in zip(means.index, means.values):
        economics = project_savings(price)
        economics["year"] = year

        economics = economics.agg(economics_agg)
        projects.append(economics)

    ds = pd.concat(projects, axis=1).T
    ds = ds.sort_values("year")
    table = pathlib.Path("./tables/table1.md")
    print(f"writing to {table}")
    table.write_text(ds.to_markdown(index=False))

    f = plot_project_savings(ds)
    out = base / "f1.png"
    print(f"plot to {out}")
    f.savefig(out)

    #  compare with the typical year forecast price
    forecast = pd.read_parquet("./data/tmy-forecast.parquet")
    ty_mean = forecast["price"].mean()
    ty_economics = project_savings(ty_mean)
    ty_economics["year"] = 2052
    projects.append(ty_economics.agg(economics_agg))

    ds = pd.concat(projects, axis=1).T
    ds = ds.sort_values("cumulative_savings_$")
    f = plot_project_savings(ds, include_project_text=False, include_tmy_text=True)

    out = base / "f5.png"
    print(f"plot to {out}")
    f.savefig(out)
