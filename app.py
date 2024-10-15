import streamlit as st
from document_manager import render_document_manager
from document_bundler import render_document_bundler

def main():
    st.set_page_config(page_title="Document Bundel App", page_icon="📁", layout="wide")
    
    st.sidebar.title("Navigatie")
    page = st.sidebar.radio("Ga naar", ["Document Bundelen", "Document Beheer"])

    if page == "Document Bundelen":
        render_document_bundler()
    elif page == "Document Beheer":
        render_document_manager()

    st.sidebar.info("Deze applicatie is ontwikkeld om het bundelen van documenten te vereenvoudigen.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Er is een onverwachte fout opgetreden: {str(e)}")