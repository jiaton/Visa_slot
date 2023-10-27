import requests
from local_io import *
from utils import *
import urllib.parse

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
        'Cookie': '_ga=GA1.2.2048602326.1698127268; _gid=GA1.2.1633399326.1698127268; _yatri_session=YhJdkM6g6yJnJ9n6L2vmKLSd%2B6XRCQOO4Om1pEmMH8T7wHViwl1BlNtzbaY5EpZliJKrzdTkOoFU52jgiKc4t710Ezr6I0AxEq61J%2Byor%2BXDjjFz1DIgCZYWWx%2FElpNnehXRbTnj99sAGT7tcai64JwOa4sx%2Fp0JXS7F812HYZhx0y%2FSsuV9Nl2vJnoJafLUGQau0AXndHHv2g3jptQPt%2FE6%2FudMnfUZwokLqSwuO2UfqEn69WOj%2FWGYRnXmxbxTIKpOLyixJafL7KMAclxPThS7FJC49WpyboZHsJFTX9ZdWhxfHPPCaz%2B9eT8jih3MbcV8m9qGYKIn%2FL6Qn2UkCbRaUCgg3Sf4wj9KI5J4XK2PwgGOVCieTKNQ%2BCePTvBTD%2FA71YkmZ63d100g3lfTMdiC--Tl1Qllz8Tg9ZywxM--4hzENu8Wm%2FAAlW83YH8oJg%3D%3D; _gat=1; _ga_W1JNKHTW0Y=GS1.2.1698131754.2.0.1698131754.0.0.0; _yatri_session=B2ILD5D1TEvitY0Tk5D5kyConQlPh4dkWDTXi5U7KYxHHukdA1sXsF1Kyr2xzFYvrQVq%2Fs7%2F8Y5R30%2BWnfvaz1b2tJlaaTYvIZmEs%2Bqp0iLGwHkVoweAAgCFylbGzzWVSz%2F3ymIziLMh5CqgbbOGZBOmLMS8oxsiELh694Hi02tG%2F5GENYrjljDX0%2BKXXT4Zi%2BFU2xTXKMwb6CYi0UmB27zZcUyCwlmtLhYvidyXtzZ4VP2mYiXWlK%2BtvZ3Jd8qUEUDSQdK30W1TiygW2Y7dCfRCc%2FrZtsT9PToQbRmDCoyX0If8TxgSei4wGDpgo4y0Mmp3Dd49aizOgFxUcTM249o85jbpXJm8t1RTFJ%2Fw3HGtHgJXqsgclom7SRQH0bUrqwJ23w4CGAMG%2FJlEveXK0YC5ge%2Bu8RIqHBOp2XsQP5XPGG9rCtGOnZXbDfsKyKssJTEIj2ncpmgbIbSdaffp2674Aa5zSahSiw8MMl5CDFCVBv6VzqHGaGrYWMCIV%2FsF70l7%2FLczhOoqn8ii9%2FlvsfB1%2F7D%2BLt%2F42PQPm2IMHWB97yEA%2BIVOgkeM0WYB06MCGEI7zNvTOLyZ66VuRTiz6aD2jTJZDPTFw64p1EaQ4kwp6QoG8cq4XVG3EJkVW4YYvX04K2XnxmvkKfGwllzFiHxg%2BwXUE%2BqzHdow4AqccYNAvSQH1Qm9OohehkKJaws6Kj3nqYkk--H8oxMlx1v%2BBb4gre--LnKVF%2FJ4K5xof0EwSRp6iA%3D%3D',
        'DNT': '1',
        'Origin': 'https://ais.usvisa-info.com',
        'Referer': 'https://ais.usvisa-info.com/en-ca/niv/users/sign_in',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-CSRF-Token': 'FEVpUC8R8W1tx+TFYY4nLugEgDaxuhSFl3Zt6sqzaybKNGCb9GQvQtq3LGbLimr5U0dsKlpErLcsJ2typPa0FA==',
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
    return yatri_session_cookie

if __name__ == '__main__':
    login()