.PHONY: setup-scratch setup fc
all: fc

setup:
	pip install poetry==1.2.2 -q
	poetry install -q

setup-scratch: setup
	nemdata -r trading-price -s 2012-01 -e 2021-12
	python ./ty/data.py

#  small hack to allow me to save plots to my blog post folder directly
#  you will want to use the default `local` to save to `./figs/*.png
PLOT-MODE ?= local
fc: setup
	python ./scripts/ty_mean.py --plot-mode $(PLOT-MODE)
	python ./scripts/motivation.py --plot-mode $(PLOT-MODE)
	python ./scripts/ty_std.py --plot-mode $(PLOT-MODE)
