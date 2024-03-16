from firebase_initializer import initialize_firebase
from firebase_admin import firestore
import pandas as pd


initialize_firebase()

collection_path = 'userCollection'


def export_to_csv(output_csv_path):
    try:
        data = []

        snapshot = firestore.client().collection(
            collection_path).get()  # 파이어베이스에서 userCollection 가져오기

        for doc in snapshot:
            data.append(doc.to_dict())

        df = pd.DataFrame(data)  # pandas 데이터로 가져오기

        df.to_csv(output_csv_path, index=False)

        print('export_to_csv 성공적으로 실행됐습니다')
    except Exception as e:
        print('export_to_csv 함수가 실행되지 않았습니다:', e)


if __name__ == '__main__':
    csv_file_path = 'data/raw/user_collection/output.csv'

    export_to_csv(csv_file_path)
