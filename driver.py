
import io
import shutil
import os.path
from os import system as sys
from magic import from_file

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from display import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def convert_bytes(size):

    for ext in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024:
            return "{} {}".format(round(size, 2), ext)
        else:
            size/= 1024

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

SERVICE = build('drive', 'v3', credentials=creds)

def fetch(PAGED_ITEMS, SERV):

    try:
        # Call the Drive v3 API
        results = SERV.files().list(
            fields="files(id, name, size)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        for item in items:

            tmp_dict = {

                    "ID":item['id'],
                    "NAME":item['name']
            }

            try:
                tmp_dict["SIZE"] = convert_bytes(int(item['size']))
                tmp_dict["TYPE"] = 'FILE'
            except KeyError:
                tmp_dict["SIZE"] = 'N/A'
                tmp_dict["TYPE"] = 'DRIVE'

            PAGED_ITEMS.append(tmp_dict)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

def inspect(args, SERV):

    datas = [SERV.files().get(fileId=arg["ID"]).execute() for arg in args]
    return datas

def clear():

    sys("clear")
    return True

def new_file(args, SERV):

    __mime = from_file(args["FILE_PATH"], mime=True)
    media = MediaFileUpload(args["FILE_PATH"], mimetype=__mime)

    try:
        file = SERV.files().create(body=args, media_body=media, fields="id").execute()
        return file.get("id")

    except HttpError as error:
        print("ERROR: {}".format(error))
        return None

def down(args, SERV):

    for arg in args:

        if arg["TYPE"] == "FILE":
            file_path = input("Enter file path for {}[relative to {}]: ".format(B(arg["NAME"]), Y(os.getcwd())))
            request = SERV.files().get_media(fileId=arg["ID"])
            fh = io.BytesIO()

            dl = MediaIoBaseDownload(fh, request, chunksize=204800)
            done = False

            try:
                while not done:
                    status, done = dl.next_chunk()

                fh.seek(0)

                with open(file_path, 'wb') as f:
                    shutil.copyfileobj(fh, f)

                print("{} Downloaded\n".format(B(arg["NAME"])))

            except:
                print(R("[ERROR] ") + "Download failed")

    return True
