# sync_launcher.py
import streamlit as st
import subprocess
import sys

st.title("🔁 Salesforce → Monday.com Sync Launcher")

if st.button("🚀 Launch Sync"):
    log_placeholder = st.empty()
    log_output = ""

    with st.spinner("Sync in progress..."):

        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            log_output += line
            log_placeholder.code(log_output)

        process.stdout.close()
        return_code = process.wait()

    if return_code == 0:
        st.success("✅ Sync completed successfully!")
    else:
        st.error(f"❌ Sync failed with return code {return_code}")
