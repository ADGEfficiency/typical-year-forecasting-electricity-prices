import pathlib


def get_plot_base(plot_mode="local"):
    if plot_mode == "local":
        base = pathlib.Path("./figs")
    else:
        assert plot_mode == "adg"
        base = pathlib.Path("../adgefficiency.github.io/assets/typical-year")
    base.mkdir(exist_ok=True)
    print(f"plot mode is {plot_mode}")
    return base
