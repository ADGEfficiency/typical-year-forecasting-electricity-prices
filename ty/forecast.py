import pandas as pd


def typical(raw: pd.DataFrame, statistic: str, month: int):

    subset = raw[raw.index.month == month]

    long_term_statistic = subset["price"].agg(statistic)

    #  groupby year and apply our statistic
    data = subset.groupby(subset.index.year)["price"].agg(statistic)
    data = data.to_frame()
    data = data.rename({"price": f"price-{statistic}"}, axis=1)
    data.index.name = "year"
    data = data.reset_index()

    #  add the month back in as an integer and as a string
    data.loc[:, "month-int"] = month
    data.loc[:, "month"] = str(list(set(subset.index.month_name()))[0])

    #  re-organize columns
    data = data[["year", "month", f"price-{statistic}", "month-int"]]

    #  add the long term statistic
    data[f"long-term-{statistic}"] = long_term_statistic
    data[f"error-{statistic}"] = abs(
        data[f"price-{statistic}"] - data[f"long-term-{statistic}"]
    )
    return data
