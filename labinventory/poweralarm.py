"""
This script will be called by the
APC Unit after 3 s of power failure
or when power comes back. Call it:
python poweralarm.py fail
python poweralarm.py clear
"""
import sys

import requests

LOGIN_URL = 'http://138.232.74.41/admin/login/'
# LOGIN_URL = 'http://127.0.0.1:8000/admin/login/'
username = "gnooki"
password = "changeme"


def main(fail_clear):
    request = requests.session()
    rsp = request.get(LOGIN_URL)
    token = rsp.cookies['csrftoken']

    rsp = request.post(
        LOGIN_URL, data={
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': token,
            'next': f'/labinventory/power-alarm/{fail_clear}/'
        })

    print(rsp.status_code, rsp.content.decode())


if __name__ == '__main__':
    main(sys.argv[1])
