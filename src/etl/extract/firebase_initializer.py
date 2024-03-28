import json
import os
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build


def initialize_firebase():
    if not firebase_admin._apps:
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


def initialize_google_analytics():
    # Load Google Analytics credentials from a JSON file
    credentials_path = os.path.join(os.path.dirname(
        __file__), '../../../config/google_analytics_4.json')
    with open(credentials_path) as f:
        json_acct_info = json.load(f)

        # analytics_config = credentials['analytics_config']

    # Create a service object for the Google Analytics Reporting API
    credentials = service_account.Credentials.from_service_account_info(
        json_acct_info)

    service = build('analyticsreporting', 'v4', credentials=credentials)

    return service
