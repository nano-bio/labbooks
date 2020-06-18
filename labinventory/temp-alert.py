# cron script for temp alert
import requests
from time import sleep

url = 'http://138.232.74.41/labinventory/temperature/is-critical/'
data = requests.get(url).json()
print("DATA:", data)

if data['is_critical']:
    import os

    for command in data['commands']:
        print("CMD:", command)
        os.system(command)
        sleep(1)
