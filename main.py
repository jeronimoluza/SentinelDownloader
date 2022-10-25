import os
import SentinelDownloader
os.system('rm -r $HOME/dhusget_tmp')
SentinelDownloader.utils.clean_dirs(['manifests'])

#geom = up.download.nominatim_osm('Rio de Janeiro', expected_position = 1)
#mercedes = 'POLYGON((-60.112229 -34.31744, -58.755617 -34.31744, -58.755617 -34.983708, -60.112229 -34.983708, -60.112229 -34.31744))'
start = '2022-09-01'
end = '2022-09-05'
pipeline_name = 'zonaba'
manifests_dir = 'manifests'
platformname = 'Sentinel-3'
product = 'OL_1_EFR___'
verbose = True
username = 'USERNAME'
password = 'PASSWORD'
processingmode = 'NT'
zonabuenosaires = 'POLYGON((-61.2736 -32.3028, -54.0606 -32.3028, -54.0606 -35.8176, -61.2736 -35.8176, -61.2736 -32.3028))'
geom = SentinelDownloader.utils.WKTtoGDF(zonabuenosaires)



dates = SentinelDownloader.utils.GetDateRange(
        start = '2022-09-01',
        end = '2022-09-05'
        )

SentinelDownloader.download.download_manifests(
    pipeline_name = 'zonaba',
    manifests_dir = 'manifests',
    #platformname = 'Sentinel-5',
    platformname = 'Sentinel-3',
    #product = 'L2__NO2___',
    #product = 'L2__HCHO__',
    product = 'OL_1_EFR___',
    dates = dates,
    geom = geom,
    verbose = True,
    processingmode = 'NT',
    username = username,
    password = password
    )

SentinelDownloader.download.download_data(
        pipeline_name = 'zonaba',
        manifests_dir = 'manifests',
        downloads_dir = 'downloads',
        semaphore = 5,
        username = username,
        password = password,
        attempts_limit = 30
)

