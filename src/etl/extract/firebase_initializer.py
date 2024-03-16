import json
import os
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    config_path = os.path.join(os.path.dirname(
        __file__), '../../../config/firebase_credentials.json')

    with open(config_path) as f:
        config = json.load(f)

    service_account_key = config['service_account_key']
    firebase_config = config['firebase_config']

    # 위에 주어진 Json account 정보로 캘박 파이어베이스 작동하는 코드
    cred = credentials.Certificate(service_account_key)
    firebase_admin.initialize_app(
        cred, {'databaseURL': firebase_config['databaseURL']})
