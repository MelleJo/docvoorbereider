import streamlit as st
import json
from create_drive_service import drive_service, list_files_in_folder

MAPPING_FILE = "document_mapping.json"
DOCUMENTS_FOLDER_ID = "your_google_drive_folder_id_here"  # Replace with your actual folder ID

def load_document_mapping():
    try:
        with open(MAPPING_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_document_mapping(mapping):
    with open(MAPPING_FILE, 'w') as f:
        json.dump(mapping, f, indent=2)

def render_document_manager():
    st.title("Document Beheer")

    mapping = load_document_mapping()
    drive_files = list_files_in_folder(DOCUMENTS_FOLDER_ID)

    col1, col2 = st.columns(2)

    with col1:
        new_quote_type = st.text_input("Nieuwe offertesoort toevoegen:")
        if st.button("Toevoegen") and new_quote_type:
            if new_quote_type not in mapping:
                mapping[new_quote_type] = []
                save_document_mapping(mapping)
                st.success(f"Offertesoort '{new_quote_type}' toegevoegd.")
            else:
                st.error("Deze offertesoort bestaat al.")

    with col2:
        quote_type_to_remove = st.selectbox("Offertesoort verwijderen:", [""] + list(mapping.keys()))
        if st.button("Verwijderen") and quote_type_to_remove:
            del mapping[quote_type_to_remove]
            save_document_mapping(mapping)
            st.success(f"Offertesoort '{quote_type_to_remove}' verwijderd.")
            st.rerun()

    st.markdown("---")

    for quote_type, documents in mapping.items():
        with st.expander(f"Documenten voor {quote_type}"):
            for doc in documents:
                col1, col2 = st.columns([3, 1])
                col1.write(doc)
                if col2.button("Verwijderen", key=f"remove_{quote_type}_{doc}"):
                    documents.remove(doc)
                    save_document_mapping(mapping)
                    st.success(f"Document '{doc}' verwijderd uit {quote_type}.")
                    st.rerun()

            available_files = [file['name'] for file in drive_files if file['name'] not in documents]
            selected_file = st.selectbox(f"Document toevoegen aan {quote_type}", [""] + available_files, key=f"select_{quote_type}")
            
            if selected_file and st.button("Toevoegen", key=f"add_{quote_type}"):
                if selected_file not in documents:
                    documents.append(selected_file)
                    save_document_mapping(mapping)
                    st.success(f"Document '{selected_file}' toegevoegd aan {quote_type}.")
                    st.rerun()
                else:
                    st.warning(f"Document '{selected_file}' is al toegevoegd aan {quote_type}.")

if __name__ == "__main__":
    render_document_manager()