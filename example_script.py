import os
import SentinelDownloader
os.system('rm -r $HOME/dhusget_tmp')
SentinelDownloader.utils.clean_dirs(['manifests'])

start = '2022-09-01'
end = '2022-09-05'
pipeline_name = 'buenosaires'
manifests_dir = 'manifests'
downloads_dir = 'downloads'
platformname = 'Sentinel-5'
product = 'L2__NO2___'
verbose = True
username = 's5pguest'
password = 's5pguest'
processingmode = 'NT'
geom_wkt = 'POLYGON((-61.2736 -32.3028, -54.0606 -32.3028, -54.0606 -35.8176, -61.2736 -35.8176, -61.2736 -32.3028))'
geom = SentinelDownloader.utils.WKTtoGDF(geom_wkt)
semaphore = 5
attempts_limit = 30


dates = SentinelDownloader.utils.GetDateRange(
        start = start,
        end = end
        )

SentinelDownloader.download.download_manifests(
    pipeline_name = pipeline_name,
    manifests_dir = manifests_dir,
    platformname = platformname,
    product = product,
    dates = dates,
    geom = geom,
    verbose = verbose,
    processingmode = processingmode,
    username = username,
    password = password
    )

SentinelDownloader.download.download_data(
        pipeline_name = pipeline_name,
        manifests_dir = manifests_dir,
        downloads_dir = downloads_dir,
        semaphore = semaphore,
        username = username,
        password = password,
        attempts_limit = attempts_limit
)

