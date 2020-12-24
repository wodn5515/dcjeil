from random import choice
import json
import string

def get_server_info_value(key: str):

    with open('server_info.json', mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v
        raise ValueError('서버정보를 확인할 수 없습니다.')

def get_filename(filename):
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return f'{pid}.{extension}'

def get_social_login_secret_key(key: str):

    with open('social_login_secret_keys.json', mode='rt', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == key:
                return v
        raise ValueError('서버정보를 확인할 수 없습니다.')