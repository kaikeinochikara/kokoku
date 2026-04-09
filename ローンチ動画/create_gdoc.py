import os
import webbrowser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = r"C:\Users\kaike\Documents\knowledge\token.json"
CREDENTIALS_PATH = r"C:\Users\kaike\Documents\knowledge\credentials.json"
MD_PATH = r"C:\Users\kaike\Documents\matsuo\ローンチ動画\【新版B】ローンチ動画台本_ゼロから新規_個別相談会誘導.md"

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]

def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds

def md_to_requests(md_text):
    """マークダウンをGoogleドキュメントのbatchUpdateリクエストに変換"""
    requests = []
    index = 1  # ドキュメント末尾の挿入位置（1スタート）

    lines = md_text.split("\n")
    # 末尾から先頭へ挿入（逆順で挿入するとインデックスがずれない）
    # ただしbatchUpdateは順番に実行されるので、先頭から末尾へ挿入し直す
    # 簡易版：全テキストを一括挿入後にスタイルを適用

    full_text = md_text
    # マークダウン記法を除去した plain text を挿入し、後でスタイルを当てる
    # ここでは簡易的に全文をそのまま挿入する
    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": full_text
        }
    })
    return requests

def create_google_doc():
    creds = get_creds()
    docs = build("docs", "v1", credentials=creds)

    # ドキュメント作成
    doc = docs.documents().create(body={"title": "【新版B】ローンチ動画台本｜ゼロから新規｜個別相談会誘導版"}).execute()
    doc_id = doc["documentId"]

    # テキスト挿入
    with open(MD_PATH, encoding="utf-8") as f:
        md_text = f.read()

    docs.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": md_to_requests(md_text)}
    ).execute()

    url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"作成完了: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    create_google_doc()
