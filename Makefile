.PHONY = create

SHELL := /bin/bash

create:
	conda create --name SDEnv python=3.7 -y;\
	pip install aiofiles aiohttp loguru pyyaml pytz requests geopandas tqdm;\
	conda activate SDEnv
	echo "CREATED SDEnv ENVIRONMENT"\

	

remove:
	conda env remove --name SDEnv
