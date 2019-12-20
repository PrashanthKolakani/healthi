age_token = None
while True:
    response = drive_service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        print (file)
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break
