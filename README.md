# Typical Year Forecasting of South Australian Electricity Prices

Supporting code for the blog post [Typical Year Forecasting of Electricity Prices](https://adgefficiency.com/typical-year-forecasting-electricity-prices).

## Use

Data for the analysis is included as a single parquet file in `./data/trading-price.parquet`.

You can reproduce the analysis by running the `make` command below (you will need Python 3.10 or above):

```shell
$ make
```

This will install Python dependencies with Poetry and run three Python scripts (they need to be run in a specific order).
