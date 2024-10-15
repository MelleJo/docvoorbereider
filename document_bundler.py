import streamlit as st
import os
import zipfile
import io
from document_manager import load_document_mapping, DOCUMENTS_DIR

def bundle_documents(quote_type):
    mapping = load_document_mapping()
    if quote_type not in mapping:
        st.error(f"Offertesoort '{quote_type}' niet gevonden.")
        return None

    document_files = mapping[quote_type]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for doc in document_files:
            file_path = os.path.join(DOCUMENTS_DIR, doc)
            if os.path.exists(file_path):
                zip_file.write(file_path, doc)
            else:
                st.warning(f"Document '{doc}' niet gevonden en overgeslagen.")
    
    zip_buffer.seek(0)
    return zip_buffer

def render_document_bundler():
    st.title("Document Bundel App")
    st.write("Selecteer een offertesoort om de vereiste documenten te bundelen.")

    mapping = load_document_mapping()
    quote_type = st.selectbox("Selecteer offertesoort:", [""] + list(mapping.keys()))
    
    if quote_type:
        st.write("Documenten in deze bundel:")
        for doc in mapping[quote_type]:
            st.write(f"- {doc}")

        if st.button("Bundel Documenten"):
            with st.spinner(f"Documenten worden gebundeld voor {quote_type}..."):
                bundled_docs = bundle_documents(quote_type)
                if bundled_docs:
                    st.success("Documenten succesvol gebundeld!")
                    st.download_button(
                        label="Download gebundelde documenten",
                        data=bundled_docs,
                        file_name=f"{quote_type}_documenten.zip",
                        mime="application/zip"
                    )
                else:
                    st.error("Er is een fout opgetreden bij het bundelen van de documenten.")
    else:
        st.info("Selecteer een offertesoort om te beginnen.")

if __name__ == "__main__":
    render_document_bundler()