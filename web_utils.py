import requests
from local_io import *
from utils import *
import urllib.parse
from bs4 import BeautifulSoup
import requests
from local_io import *
import json
from datetime import datetime, timedelta

from utils import *

from email_utils import send_email
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

def get_headers(yatri_session_cookie, csrf_token):
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
    'Cookie': f'_yatri_session={yatri_session_cookie}',
    'X-CSRF-Token': f'{csrf_token}'
    }
    return headers
def login():
    print('login...')
    url = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
    login_email = load_config()()['login_email']
    login_password = load_config()()['login_password']
    payload = f"user%5Bemail%5D={urllib.parse.quote(login_email)}&user%5Bpassword%5D={urllib.parse.quote(login_password)}&policy_confirmed=1&commit=Sign+In"
    headers = {
        'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Cookie': '_ga=GA1.2.2048602326.1698127268; _gid=GA1.2.1633399326.1698127268; _yatri_session=YhJdkM6g6yJnJ9n6L2vmKLSd%2B6XRCQOO4Om1pEmMH8T7wHViwl1BlNtzbaY5EpZliJKrzdTkOoFU52jgiKc4t710Ezr6I0AxEq61J%2Byor%2BXDjjFz1DIgCZYWWx%2FElpNnehXRbTnj99sAGT7tcai64JwOa4sx%2Fp0JXS7F812HYZhx0y%2FSsuV9Nl2vJnoJafLUGQau0AXndHHv2g3jptQPt%2FE6%2FudMnfUZwokLqSwuO2UfqEn69WOj%2FWGYRnXmxbxTIKpOLyixJafL7KMAclxPThS7FJC49WpyboZHsJFTX9ZdWhxfHPPCaz%2B9eT8jih3MbcV8m9qGYKIn%2FL6Qn2UkCbRaUCgg3Sf4wj9KI5J4XK2PwgGOVCieTKNQ%2BCePTvBTD%2FA71YkmZ63d100g3lfTMdiC--Tl1Qllz8Tg9ZywxM--4hzENu8Wm%2FAAlW83YH8oJg%3D%3D; _gat=1; _ga_W1JNKHTW0Y=GS1.2.1698131754.2.0.1698131754.0.0.0',
        'X-CSRF-Token': 'FEVpUC8R8W1tx+TFYY4nLugEgDaxuhSFl3Zt6sqzaybKNGCb9GQvQtq3LGbLimr5U0dsKlpErLcsJ2typPa0FA==',
        'Origin': 'https://ais.usvisa-info.com',
        'Referer': 'https://ais.usvisa-info.com/en-ca/niv/users/sign_in',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
}
    session = requests.Session()
    response = session.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    # print(response.headers)
    yatri_session_cookie = session.cookies.get('_yatri_session')
    # log(f'login cookie: {yatri_session_cookie}')
    # print(yatri_session_cookie)
    save_cookie_to_file(yatri_session_cookie, 'cookie.txt')
    return yatri_session_cookie, session
def get_cstf(session):
    url = "https://ais.usvisa-info.com/en-ca/niv/schedule/52876573/appointment"
    payload={}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://ais.usvisa-info.com/en-ca/niv/schedule/52876573/continue_actions',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = session.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
    return csrf_token

def try_once(url, place, csrf_token, yatri_session_cookie):
    payload={}
    # yatri_session_cookie = read_cookie_from_file('cookie.txt')
    headers= get_headers(yatri_session_cookie, csrf_token)
    

    response = requests.request("GET", url=url, headers=headers, data=payload)

    # print(response.text)
    if "expired" in response.text or "error" in response.text:
        print('cookie expired, need to login')
        yatri_session_cookie = login()
        headers= get_headers(yatri_session_cookie, csrf_token)
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
        log(f'Access banned, need to switch IP.')
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
    yatri_session_cookie, session = login()
    csrf_token = get_cstf(session)
    print(csrf_token)
    url_dict = load_config()()['url_dict']
    url, place = url_dict['vancouver'], 'vancouver'
    try_once(url, place, csrf_token, yatri_session_cookie)