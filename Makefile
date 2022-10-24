.PHONY = create

SHELL := /bin/bash

create:
	conda create --name SDEnv python=3.7 -y;\
	source activate SDEnv; \
    pip install aiofiles aiohttp loguru pyyaml pytz requests geopandas tqdm;

remove:
	conda env remove --name SDEnv
