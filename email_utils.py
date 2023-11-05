import yagmail
from utils import *
def send_email(receiver, contents, subject, play_sound=False):
    log(f'Sending email to {receiver}')
    sender = load_config()()['sender']
    password = load_config()()['password']
    yag = yagmail.SMTP(sender, password)
    yag.send(receiver, subject, contents)
    
if __name__ == '__main__':
    receiver = load_config()()['receiver']
    contents = ['This is the body, and here is just text http://somedomain/image.png',
                'You can find an audio file attached.', '/local/path/song.mp3']
    send_email(receiver, contents, 'test subject')