from datetime import datetime, timedelta
import yaml

def log(message):      
    print(message)
    
    with open(f'running.log', 'a') as f:
        if message == '':
            f.write('\n')
        else:    
            f.write(f'{datetime.now()} - {message}\n')
            
def load_config():
    def read_config():  
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            
            sender = config['email']['sender']
            password = config['email']['password']
            receiver = config['email']['receiver']

            urls = config['urls']
            url_dict = {}
            for url in urls:
                city = url['city']
                url_str = url['url']
                url_dict[city] = url_str
            
            start_date_str = config['dates']['start_date']
            end_date_str = config['dates']['end_date']

            login_email = config['ais_credentials']['email']
            login_password = config['ais_credentials']['password']
            
            no_payments_account_credentials = config['no_payments_account_credentials']
              
        return {'sender': sender, 
                'password': password, 
                'receiver': receiver, 
                'url_dict': url_dict,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'login_email': login_email,
                'login_password': login_password,
                'no_payments_accounts': no_payments_account_credentials,
                }
    config_cache = None
    
    def get_config():
        nonlocal config_cache
        if config_cache is None:
            config_cache = read_config()
        return config_cache
    return get_config

def get_account_from_pool():
    no_payments_accounts = load_config()()['no_payments_accounts']
    length = len(no_payments_accounts)
    curr = [0]
    def generate():
        ret = no_payments_accounts[curr[0]]
        curr[0] += 1
        curr[0] %= length
        return ret
    return generate