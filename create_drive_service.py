import streamlit as st
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def create_drive_service():
    creds = Credentials.from_authorized_user_info(st.secrets["google_credentials"])
    return build('drive', 'v3', credentials=creds)

drive_service = create_drive_service()

def get_file_content(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    return request.execute()