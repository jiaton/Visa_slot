from web_utils import *
from local_io import *
from datetime import datetime, timedelta
import time
from utils import *
import random
from email_utils import send_email
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

def main(enable_vpn = False):
    url_dict = load_config()()['url_dict']
    no_payments_accounts = load_config()()['no_payments_accounts']
    global VPN_settings 
    if enable_vpn:
        VPN_settings = initialize_VPN(stored_settings=0,save=0,area_input=['complete rotation'],skip_settings=None)
    
    # login_email = load_config()()['login_email']
    # login_password = load_config()()['login_password']
    # yatri_session_cookie, session = login(login_email, login_password)
    # csrf_token = get_cstf(session)
    
    now = datetime.now()
    next_interval = (now + timedelta(minutes=0)).replace(second=0, microsecond=0)
    
    is_healthy = True
    # while True:
    #     now = datetime.now()
    #     if now >= next_interval:
    #         for city, url in url_dict.items():
    #             is_healthy = try_once_main_account(url, city, csrf_token, yatri_session_cookie)
    #             time.sleep(3)
    #         if is_healthy:
    #             next_interval = (now + timedelta(minutes=random.randint(2, 4))).replace(second=0, microsecond=0)
    #         else:
    #             next_interval = (now + timedelta(minutes=100)).replace(second=0, microsecond=0)
    #             if enable_vpn:
    #                 log(f'Switching IP...')
    #                 rotate_VPN(instructions=VPN_settings, google_check = 0) 
    #         log(f'Next try at {next_interval}')
    #     time.sleep(1)
    
    account_generator = get_account_from_pool()
    no_payments_account = account_generator()    
    yatri_session_cookie, session = login(no_payments_account['email'],  no_payments_account['password'])
    csrf_token = get_cstf(session)
    counts = 20
    while True:
        now = datetime.now()
        if now >= next_interval:
            counts -= 1
            city_dict = try_once_free_account(no_payments_account['payment_url'], csrf_token, yatri_session_cookie)
            if not city_dict:
                # switch account
                no_payments_account = account_generator()    
                yatri_session_cookie, session = login(no_payments_account['email'],  no_payments_account['password'])
                csrf_token = get_cstf(session)
                
            next_interval = (now + timedelta(minutes=1)).replace(microsecond=0)
            log(f'Next try at {next_interval}')
        time.sleep(1)
            
        
if __name__ == '__main__':
    main(enable_vpn = False)