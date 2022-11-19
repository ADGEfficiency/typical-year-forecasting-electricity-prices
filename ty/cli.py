import argparse


def cli():
    """determines where plots are saved"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plot-mode", default="local", nargs="?", type=str, const="local"
    )
    return parser.parse_args()
