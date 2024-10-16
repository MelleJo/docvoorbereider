quote_type = st.selectbox("Selecteer offerte type:", list(document_mapping.keys()))
if st.button("Bundel de documenten"):
    st.write(f"Bezig met het voorbereiden voor: {quote_type}...")
    # Call function to bundle documents (implement in next step)