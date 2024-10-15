quote_type = st.selectbox("Select quote type:", list(document_mapping.keys()))
if st.button("Bundle Documents"):
    st.write(f"Bundling documents for {quote_type}...")
    # Call function to bundle documents (implement in next step)