.PHONY: setup-scratch setup fc
all: fc

#  small hack to allow me to save plots to my blog post folder directly
#  you will want to use the default `local` to save to `./figs/*.png
PLOT-MODE ?= local
setup-scratch: setup
	git clone git@github.com:ADGEfficiency/nem-data.git
	cd nem-data; git checkout 2d72dbd819fe88803195cadb2ad0d9b3b3dc840f; make setup; cd ..
	nem --reports trading-price --start 2012-01 --end 2021-12
	python ./ty/data.py

setup:
	poetry install

fc: setup
	python ./scripts/ty_mean.py --plot-mode $(PLOT-MODE)
	python ./scripts/motivation.py --plot-mode $(PLOT-MODE)
	python ./scripts/ty_std.py --plot-mode $(PLOT-MODE)
