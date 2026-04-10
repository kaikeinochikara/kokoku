import webbrowser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = r"C:\Users\kaike\Documents\knowledge\token.json"
MD_PATH = r"C:\Users\kaike\Documents\matsuo\ローンチ動画\【新版E】ローンチ動画台本_AI時代の管理会計_簿記1級訴求.md"
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]

def get_creds():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds

def create_google_doc():
    creds = get_creds()
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().create(body={"title": "【新版E】ローンチ動画台本｜AI時代の管理会計×簿記1級訴求"}).execute()
    doc_id = doc["documentId"]
    with open(MD_PATH, encoding="utf-8") as f:
        md_text = f.read()
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": 1}, "text": md_text}}]}
    ).execute()
    url = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(url)
    webbrowser.open(url)

if __name__ == "__main__":
    create_google_doc()
