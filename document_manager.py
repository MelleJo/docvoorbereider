import streamlit as st
import os
import json
import shutil

DOCUMENTS_DIR = "documents"
MAPPING_FILE = "document_mapping.json"

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
                    file_path = os.path.join(DOCUMENTS_DIR, doc)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    save_document_mapping(mapping)
                    st.success(f"Document '{doc}' verwijderd uit {quote_type}.")
                    st.rerun()

            uploaded_file = st.file_uploader(f"Document toevoegen aan {quote_type}", key=f"upload_{quote_type}")
            if uploaded_file:
                if uploaded_file.name.lower().endswith('.pdf'):
                    file_path = os.path.join(DOCUMENTS_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    if uploaded_file.name not in documents:
                        documents.append(uploaded_file.name)
                        save_document_mapping(mapping)
                        st.success(f"Document '{uploaded_file.name}' toegevoegd aan {quote_type}.")
                    else:
                        st.warning(f"Document '{uploaded_file.name}' is vervangen.")
                    st.rerun()
                else:
                    st.error("Alleen PDF-bestanden zijn toegestaan.")

if __name__ == "__main__":
    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)
    render_document_manager()