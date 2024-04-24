import json
import os
import firebase_admin
from firebase_admin import credentials
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient


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
    """Initializes a BetaAnalyticsDataClient object."""

    # Load Google Analytics credentials from a JSON file
    credentials_path = os.path.join(os.path.dirname(
        __file__), '../../../config/google_analytics_4.json')
    with open(credentials_path) as f:
        json_acct_info = json.load(f)

    # Create credentials object with the required scope
    credentials = Credentials.from_service_account_info(
        json_acct_info).with_scopes(["https://www.googleapis.com/auth/analytics.readonly"])

    # Create a BetaAnalyticsDataClient object
    client = BetaAnalyticsDataClient(credentials=credentials)

    return client
