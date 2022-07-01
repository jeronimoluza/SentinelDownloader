# S5P

This repository contains code to download and process Sentinel 5P satellite products **(currently supporting NO2 only)**.

>The Copernicus Sentinel-5 Precursor mission is the first Copernicus mission dedicated to monitoring our atmosphere. Copernicus Sentinel-5P is the result of close collaboration between ESA, the European Commission, the Netherlands Space Office, industry, data users and scientists. The mission consists of one satellite carrying the TROPOspheric Monitoring Instrument (TROPOMI) instrument. The TROPOMI instrument was co-funded by ESA and The Netherlands.
>
>The main objective of the Copernicus Sentinel-5P mission is to perform atmospheric measurements with high spatio-temporal resolution, to be used for air quality, ozone & UV radiation, and climate monitoring & forecasting.

Open access data hub: https://scihub.copernicus.eu/dhus/#/home


This code operates through main.py using arguments as follows:

*python main.py -arg*

List of arguments:

* **download_data**: downloads Sentinel 5P manifests for retrieving data and proceeds to download netCDF4 files for NO2 data from 2018-10-17 to 9 days before today's date. Skips files that already exists in the downloaded files folder (skips manifests & nc files).
* **download_broken**: checks for broken netCDF4 files and downloads them again. Also downloads any missing nc files that are stated on the manifests but couldn't be found on the download folder.
* **check_database**: checks existing database and outputs files left to process (NC to ORC).
* **nc_to_orc**: reads all nc files and process them to point data (**pixel centroids**) in ORC format. *src folder contains a script for doing this in parallel*.
