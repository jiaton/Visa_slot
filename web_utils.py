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
def login(login_email, login_password):
    print('login...')
    url = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
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
    # save_cookie_to_file(yatri_session_cookie, 'cookie.txt')
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
def check_good_date(date):
    start_date = datetime.strptime(load_config()()['start_date'], '%m-%d-%Y')
    end_date = datetime.strptime(load_config()()['end_date'], '%m-%d-%Y')
    if start_date <= date <= end_date:
        return True
def try_once_main_account(url, place, csrf_token, yatri_session_cookie):
    payload={}
    # yatri_session_cookie = read_cookie_from_file('cookie.txt')
    headers= get_headers(yatri_session_cookie, csrf_token)
    

    response = requests.request("GET", url=url, headers=headers, data=payload)

    # print(response.text)
    if "expired" in response.text or "error" in response.text:
        print('cookie expired, need to login')
        yatri_session_cookie, session = login()
        csrf_token = get_cstf(session)
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
        send_email(receiver, contents, f'Found dates available in {place}!!!', True)
    return True

def try_once_free_account(payment_url, csrf_token, yatri_session_cookie):
    payload={}
    headers= get_headers(yatri_session_cookie, csrf_token)
    try:
        response = requests.request("GET", url=payment_url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'for-layout'})
        rows = table.find_all('tr')
    except:
        log(f'Access banned.')
        return False
    date_dict = {}
    url_dict = load_config()()['url_dict']
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        if 'No Appointments Available' in cols[1]:
            continue
        city_name, earlist_available_date = cols[0].lower(), datetime.strptime(cols[1], '%d %B, %Y')
        if city_name not in url_dict:
            continue
        date_dict[city_name] = earlist_available_date
    if len(date_dict) == 0:
        log(f'Access banned.')
        return False
    for city_name, earlist_available_date in date_dict.items():
        log(f'{city_name}: {earlist_available_date.strftime("%Y-%m-%d")}')
        if check_good_date(earlist_available_date):
            log(f'{earlist_available_date} available in {city_name}')
            receiver = load_config()()['receiver']
            contents = [f'Found dates available in {city_name}',
                    f'Earlist available date: {earlist_available_date}'
                    ]
            send_email(receiver, contents, f'Found dates available in {city_name}!!!', True)
    return date_dict
        
    
if __name__ == '__main__':
    # login_email = load_config()()['login_email']
    # login_password = load_config()()['login_password']
    # yatri_session_cookie, session = login()
    # csrf_token = get_cstf(session)
    # print(csrf_token)
    # url_dict = load_config()()['url_dict']
    # url, place = url_dict['vancouver'], 'vancouver'
    # try_once_main_account(url, place, csrf_token, yatri_session_cookie)
    
    free_account_url = 'https://ais.usvisa-info.com/en-ca/niv/schedule/53027427/payment'
    login_email = "javzzzzh@gmail.com"
    login_password = "9VPpcmAaUJowvRa"
    yatri_session_cookie, session = login(login_email, login_password)
    csrf_token = get_cstf(session)
    print(csrf_token)
    date_dict = try_once_free_account(free_account_url, csrf_token, yatri_session_cookie)
    print(date_dict)