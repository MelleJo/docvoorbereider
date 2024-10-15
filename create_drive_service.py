import streamlit as st
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def create_drive_service():
    creds = None
    if 'token' in st.session_state:
        creds = Credentials.from_authorized_user_info(st.session_state.token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = Credentials.from_authorized_user_info({
                'client_id': st.secrets['google_oauth']['client_id'],
                'client_secret': st.secrets['google_oauth']['client_secret'],
                'refresh_token': st.secrets['google_oauth']['refresh_token']
            })

        # Save the credentials for the next run
        st.session_state.token = creds.to_json()

    return build('drive', 'v3', credentials=creds)

drive_service = create_drive_service()

def list_files_in_folder(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    return results.get('files', [])

def get_file_content(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    return request.execute()