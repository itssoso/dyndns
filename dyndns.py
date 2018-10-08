import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GODADDY_DOMAIN = os.getenv('GODADDY_DOMAIN')
GODADDY_KEY = os.getenv('GODADDY_KEY')
GODADDY_SECRET = os.getenv('GODADDY_SECRET')


def get_current_ip():
    req = requests.get('https://api.ipify.org?format=json')
    return req.json()['ip']


def get_record_info(type='A', name='@'):
    url = 'https://api.godaddy.com/v1/domains/{}/records/{}/{}'
    url = url.format(GODADDY_DOMAIN, type, name)
    headers = {
        'Authorization': 'sso-key {}:{}'.format(
            GODADDY_KEY,
            GODADDY_SECRET
        )
    }
    resp = requests.get(url, headers=headers)
    return resp.json()


def update_dns(current_ip, type='A', name='@', ttl=600):
    url = 'https://api.godaddy.com/v1/domains/{}/records/{}/{}'
    url = url.format(GODADDY_DOMAIN, type, name)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        'Authorization': 'sso-key {}:{}'.format(
            GODADDY_KEY,
            GODADDY_SECRET
        )
    }
    data = json.dumps([{
        "data": current_ip,
        "ttl": ttl,
        "name": name,
        "type": type
    }]).encode('utf-8')
    resp = requests.put(url, headers=headers, data=data)
    return resp.text


def main():
    current_ip = get_current_ip()
    resp = get_record_info()[0]
    if resp['data'] != current_ip:
        print("IP is different...")
        print("IP before:", resp['data'])
        print("IP after:", current_ip)
        update_resp = update_dns(current_ip)
        print("Updating IP:", update_resp)


if __name__ == '__main__':
    main()
