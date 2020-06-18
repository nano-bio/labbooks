# raspi script to measure temperature and send to labbook server
import requests

sensors = [{
    'name': "temp_sensor_1",  # prevacuum
    'hardware_path': "28-00000c37704e"
}, {
    'name': "temp_sensor_2",  # big lab
    'hardware_path': "28-00000c370c59"
}]
response = {'passphrase': 'K+4BP6JdySD%dpc-w58Wp?qnHmdQ=&RuuL47Wt+A'}
for sensor in sensors:
    try:
        with open("/sys/bus/w1/devices/{}/w1_slave".format(sensor['hardware_path']), 'r') as f:
            lines = f.readlines()
            temp = int(lines[1].split('t=')[1].strip()) / 1000
            response[sensor['name']] = temp
    except Exception as e:
        print(e)

print(response)

r = requests.post('http://138.232.74.41/labinventory/temperature/put/', json=response)

print(r.status_code)
