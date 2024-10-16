import streamlit as st
from document_bundler import render_document_bundler

def main():
    st.set_page_config(page_title="Offerte documenten tool", page_icon="📁", layout="wide")
    
    st.title("Offerte documenten tool")
    render_document_bundler()

    st.sidebar.info("Dit is nog maar een test :)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Er is een onverwachte fout opgetreden: {str(e)}")