
def save_cookie_to_file(cookie_value, file_path):
    with open(file_path, 'w') as f:
        f.write(cookie_value)

def read_cookie_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()