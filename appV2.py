from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


# returns files belonging to a folder
def print_files_in_folder(service, folder_id):
  request = service.files().list(q="'{}' in parents".format(folder_id),
                                 fields="nextPageToken,incompleteSearch,files(id,mimeType,name)")
  response = request.execute()
  list = []
  for file in response.get('files', []):
     list.append(file.get('name'))
  return list


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # get the email address of the user
    about = service.about().get(fields="user").execute()
    email = about['user'].get('emailAddress')

    # get the id of the directory
    response = service.files().list(q="name='Healthi'", fields="files").execute()
    folder_id = response['files'][0].get('id')

    # to store the folder details
    dict = {}
    # to store the final result
    result = {}
    # to store the files inside Healthi folder
    list = []

    response = service.files().list(q="'{}' in parents".format(folder_id),
                                   fields="*").execute()
    for file in response.get('files', []):
        if (file.get('mimeType') == "application/vnd.google-apps.folder"):
            dict[file.get('name')] = print_files_in_folder(service, file.get('id'))
        else:
            list.append(file.get('name'))

    dict['Healthi'] = list
    result[email] = dict
    print(result)

if __name__ == '__main__':
    main()
