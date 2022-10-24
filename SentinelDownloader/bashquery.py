import datetime
import subprocess

class BashQuery:
    def __init__(
        self,
        manifest_directory: str,
        platformname: str, # Original: 'Sentinel-5'
        product: str,
        date: str,
        geom_wkt: str,
        processingmode: str = 'NT',
        username: str = 's5pguest',
        password: str = 's5pguest'
    ):
        manifest_destination = f"{manifest_directory}/{platformname}_{product}{date}.csv"

        s5p = {'NT': 'Offline', 'NR': 'Near Real Time'}
        other_sentinels = {'NR':'Near Real Time', 'NT': 'Non Time Critical'} # LEAVING OUT SENTINEL 1. CHECK https://scihub.copernicus.eu/userguide/FullTextSearch#Search_Keywords

        if platformname == 'Sentinel-5':
            hub = 's5phub'
            username = 's5pguest'
            password = 's5pguest'
            processingmode_query = f'processingmode: {s5p[processingmode]}'
        else:
            hub = 'scihub'
            processingmode_query = f'timeliness: {other_sentinels[processingmode]}'
        
        #-d "https://s5phub.copernicus.eu/dhus" \
        cmd_text = f"""sh $PWD/scripts/dhusget.sh -u "{username}" -p "{password}" \
        -d "https://{hub}.copernicus.eu/dhus" -l "100" \
        -C "{manifest_destination}" \
        -q "OSquery-result.xml" \
        -F 'platformname:{platformname} AND {processingmode_query} AND producttype:{product}\
        (beginPosition:[{date}T00:00:00.000Z TO {date}T23:59:59.999Z] AND \
        endPosition:[{date}T00:00:00.000Z TO {date}T23:59:59.999Z]) AND \
        ( footprint:"Intersects({geom_wkt})")'"""
        
        self.cmd_text = cmd_text

    def see_query(self):
        return self.cmd_text

    def execute(self):
        subprocess.call(
            self.cmd_text,
            shell=True,
            executable='/bin/bash',
        )
    
    def silent_execute(self):
        subprocess.call(
            self.cmd_text,
            shell=True,
            executable='/bin/bash',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)