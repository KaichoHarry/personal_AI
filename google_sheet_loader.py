# google_sheet_loader.py
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# ----------------------------------------
# 設定： spreadsheet_id と range を適宜変更
# ----------------------------------------
SPREADSHEET_ID = "1NjC9hIuTSL5-2ZvFdbs21rbxRRT2eCfvTA-pXVyMbd8"
RANGE_NAME = "フォームの回答 1!A:Z"  # シート名に合わせる

def load_google_sheet(credentials_path="credentials.json"):
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])
    if not values:
        return pd.DataFrame()
    # 1行目をヘッダーとする
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

if __name__ == "__main__":
    df = load_google_sheet()
    print(df.head())
