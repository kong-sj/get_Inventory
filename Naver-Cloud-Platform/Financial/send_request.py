import requests

def send_request(url, headers, method):
    r = requests.request(method, url, headers=headers)
    if r.status_code != 200:
        print('ERROR! {} {}'.format(r.status_code, r.text))
    return r.text