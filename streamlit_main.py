import streamlit as st
import subprocess
import sys

st.title("📊 Salesforce ↔ Monday.com Sync Tool")

if st.button("🔄 Sync Items from Salesforce"):
    with st.spinner("Running item sync..."):
        result = subprocess.run([sys.executable, "main.py", "sync"], capture_output=True, text=True)
        st.code(result.stdout)
        if result.stderr:
            st.error(result.stderr)
        else:
            st.success("✅ Salesforce items synced!")

if st.button("🔗 Connect Boards"):
    with st.spinner("Running board linking..."):
        result = subprocess.run([sys.executable, "main.py", "link"], capture_output=True, text=True)
        st.code(result.stdout)
        if result.stderr:
            st.error(result.stderr)
        else:
            st.success("✅ Boards linked!")