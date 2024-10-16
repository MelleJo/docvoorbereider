import streamlit as st
import io
import zipfile
from create_drive_service import drive_service, get_file_content

DOCUMENTS_FOLDER_ID = "your_google_drive_folder_id_here"  # Replace with your actual folder ID

def list_files_in_folder(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/pdf'",
        pageSize=1000,
        fields="nextPageToken, files(id, name)"
    ).execute()
    return results.get('files', [])

def bundle_documents(selected_files):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in selected_files:
            file_content = get_file_content(file['id'])
            zip_file.writestr(file['name'], file_content)
    
    zip_buffer.seek(0)
    return zip_buffer

def render_document_bundler():
    st.write("Selecteer de documenten die u wilt bundelen.")

    files = list_files_in_folder(DOCUMENTS_FOLDER_ID)
    file_names = [file['name'] for file in files]
    
    selected_file_names = st.multiselect("Selecteer documenten:", file_names)
    
    if selected_file_names:
        selected_files = [file for file in files if file['name'] in selected_file_names]
        
        if st.button("Bundel Documenten"):
            with st.spinner("Documenten worden gebundeld..."):
                bundled_docs = bundle_documents(selected_files)
                if bundled_docs:
                    st.success("Documenten succesvol gebundeld!")
                    st.download_button(
                        label="Download gebundelde documenten",
                        data=bundled_docs,
                        file_name="gebundelde_documenten.zip",
                        mime="application/zip"
                    )
                else:
                    st.error("Er is een fout opgetreden bij het bundelen van de documenten.")
    else:
        st.info("Selecteer minimaal één document om te bundelen.")

if __name__ == "__main__":
    render_document_bundler()