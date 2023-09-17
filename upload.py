import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# OAuth 2.0 setup
CLIENT_SECRETS_FILE = "./path_to_client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)


def upload_video(youtube, file):
    body = {
        'snippet': {
            'title': 'hellO!',
            'description': 'Your Video Description',
            'tags': ['sample', 'video', 'example'],
            'categoryId': '22'  # Entertainment category
        },
        'status': {
            'privacyStatus': 'unlisted'  # or 'private' or 'public'
        }
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype='video/*')
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")

if __name__ == '__main__':
    youtube = get_authenticated_service()
    file = './results/Askreddit/If someone gave you 1000 a day to never drink alcohol againever what would you do.mp4'
    try:
        upload_video(youtube, file)
    except HttpError as e:
        print(f"An error occurred: {e}")