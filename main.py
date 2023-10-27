import requests
from login import login
from local_io import *
import json
from datetime import datetime, timedelta
import time
from utils import *
import random
from email_utils import send_email
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

def get_headers(yatri_session_cookie):
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'DNT': '1',
    'If-None-Match': 'W/"b2bfdb5b62dcf13a6c98d77dbf7cbb13"',
    'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/52876573/appointment',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': f'_yatri_session={yatri_session_cookie}'
    }
    return headers
    
def try_once(url, place):
    payload={}
    yatri_session_cookie = read_cookie_from_file('cookie.txt')
    headers= get_headers(yatri_session_cookie)
    

    response = requests.request("GET", url=url, headers=headers, data=payload)

    # print(response.text)
    if "expired" or "error" in response.text:
        print('cookie expired, need to login')
        yatri_session_cookie = login()
        headers= get_headers(yatri_session_cookie)
        response = requests.request("GET", url=url, headers=headers, data=payload)

    response_json = json.loads(response.text)

    dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in response_json]
    start_date = datetime.strptime(load_config()()['start_date'], '%m-%d-%Y')
    end_date = datetime.strptime(load_config()()['end_date'], '%m-%d-%Y')
    good_dates = []
    for date in dates:
        if start_date <= date <= end_date:
            log(f'{date} available in {place}')
            good_dates.append(date)
    if len(dates) > 0:
        log(f'Earlist available date in {place}: {min(dates)}')
    else:
        log(f'Access banned, rotating VPN...')
        # rotate_VPN(instructions=VPN_settings, google_check = 0) # todo
        return False
    log(f'{len(good_dates)} available in {place}: {good_dates}')
    
    if len(good_dates) > 0:
        receiver = load_config()()['receiver']
        contents = [f'Found dates available in {place}',
                    f'Earlist available date: {min(dates)}',
                    f'All good dates: {good_dates}']
        send_email(receiver, contents, f'Found dates available in {place}!!!')
    return True

if __name__ == '__main__':
    url_dict = load_config()()['url_dict']
    global VPN_settings 
    # VPN_settings = initialize_VPN(stored_settings=0,save=0,area_input=['complete rotation'],skip_settings=None)

    now = datetime.now()
    next_interval = (now + timedelta(minutes=0)).replace(second=0, microsecond=0)
    is_healthy = True
    while True:
        now = datetime.now()
        if now >= next_interval:
            for city, url in url_dict.items():
                is_healthy = try_once(url, city)
                time.sleep(3)
            if is_healthy:
                next_interval = (now + timedelta(minutes=random.randint(3, 4))).replace(second=0, microsecond=0)
            else:
                next_interval = (now + timedelta(minutes=3)).replace(second=0, microsecond=0)
            log(f'Next try at {next_interval}')
        time.sleep(1)