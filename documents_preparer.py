import streamlit as st
import io
import zipfile
from document_api import get_document_from_drive
from document_mapping import document_mapping
import magic  # for MIME type checking

def is_pdf(file_content):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_content)
    return file_type == 'application/pdf'

def bundle_documents(quote_type):
    document_ids = document_mapping[quote_type]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for doc_id in document_ids:
            file = get_document_from_drive(doc_id)
            if not is_pdf(file.getvalue()):
                st.error(f"Bestand {doc_id} is geen PDF. Bundelen geannuleerd.")
                return None
            zip_file.writestr(f"document_{doc_id}.pdf", file.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer

def render_document_bundler():
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #0066cc;
        color: white;
    }
    .stSelectbox {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Offerte documenten tool")
    st.write("Selecteer een offertesoort om de vereiste documenten te bundelen.")

    quote_type = st.selectbox("Selecteer offertesoort:", list(document_mapping.keys()))
    if st.button("Bundel Documenten"):
        with st.spinner("Documenten worden gebundeld voor {quote_type}..."):
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

if __name__ == "__main__":
    render_document_bundler()