import streamlit as st
import subprocess

st.title('Salesforce <> Monday.com Sync Launcher')

if st.button("launch sync"):
    with st.spinner("launching sync..."):
        # Run the sync script
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)

    if result.returncode == 0:
        st.success("✅ Sync completed successfully!")
        st.text(result.stdout)
    else:
        st.error("❌ Error occurred")
        st.text(result.stderr)