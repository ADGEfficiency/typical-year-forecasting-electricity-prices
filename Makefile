all: fc

PLOT-MODE ?= local

setup-scratch: setup
	git clone git@github.com:ADGEfficiency/nem-data.git
	# cd nem-data; git checkout 7cd3c069b5fa4ba24c8c3673405551e4feecd401: make setup; cd ..
	cd nem-data; git checkout master; make setup; cd ..
	nem --reports trading-price --start 2012-01 --end 2021-12
	python ./ty/data.py

setup:
	poetry install

fc: setup
	python ty_mean.py --plot-mode $(PLOT-MODE)
	python motivation.py --plot-mode $(PLOT-MODE)
	python ty_std.py --plot-mode $(PLOT-MODE)
