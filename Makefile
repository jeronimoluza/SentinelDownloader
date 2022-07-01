.PHONY = create

SHELL := /bin/bash

REPO=$(shell basename $(CURDIR))

create:
	conda create --name $(REPO) python=3.7 -y;\
	source activate $(REPO); \
    conda install ipython ipykernel -y; \
    pip install netCDF4 aiofiles aiohttp loguru pyyaml pytz pandas requests pyarrow argparse; \
	python -m ipykernel install --user --name=$(REPO);
