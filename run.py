import fire
import os
import SentinelDownloader
os.system('rm -r $HOME/dhusget_tmp')

class S5PDownloader(object):
        """Class for Fire CLI operation."""


        def download_manifests(
                self,
                start_date,
                end_date,
                pipeline_name,
                manifests_dir,
                platformname,
                product,
                geom_wkt,
                verbose,
                processingmode,
                username,
                password
        ):      
                dates = SentinelDownloader.utils.GetDateRange(
                        start = start_date,
                        end = end_date
                        )

                geom = SentinelDownloader.utils.WKTtoGDF(geom_wkt)

                SentinelDownloader.download.download_manifests(
                        pipeline_name = pipeline_name,
                        manifests_dir = manifests_dir,
                        platformname = platformname,
                        product = product,
                        dates = dates,
                        geom = geom,
                        verbose = True,
                        processingmode = 'NT',
                        username = username,
                        password = password
                        )

        def download_data(
                self,
                pipeline_name,
                manifests_dir,
                downloads_dir,
                username,
                password,
                semaphore = 5,
                attempts_limit = 30
        ):
                """_summary_

                Args:
                    pipeline_name (_type_): _description_
                    manifests_dir (_type_): _description_
                    downloads_dir (_type_): _description_
                    username (_type_): _description_
                    password (_type_): _description_
                    semaphore (int, optional): _description_. Defaults to 5.
                    attempts_limit (int, optional): _description_. Defaults to 30.
                """
                SentinelDownloader.download.download_data(
                        pipeline_name = pipeline_name,
                        manifests_dir = manifests_dir,
                        downloads_dir = downloads_dir,
                        semaphore = semaphore,
                        username = username,
                        password = password,
                        attempts_limit = attempts_limit
                        )
        
        def config_run(
                self,
                config_path
        ):
                SentinelDownloader.download.config_run(config_path)

if __name__ == '__main__':
        fire.Fire(S5PDownloader)