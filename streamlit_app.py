# streamlit_app.py
import streamlit as st
import subprocess

st.set_page_config(page_title="Salesforce → Monday.com Sync Tool", layout="centered")

st.title("🔁 Salesforce → Monday.com Sync Tool")

st.markdown("Use the buttons below to control synchronization and linking.")

# 버튼 1: 레코드 업데이트
if st.button("🔄 Sync Records (Salesforce → Monday.com)"):
    with st.spinner("Syncing records..."):
        result = subprocess.run(["python", "sync_launcher.py"], capture_output=True, text=True)
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("✅ Sync completed successfully!")
        else:
            st.error("❌ Sync failed.")
            st.code(result.stderr)

# 버튼 2: 보드 간 연결
if st.button("🔗 Link Boards in Monday.com"):
    with st.spinner("Linking boards..."):
        result = subprocess.run(["python", "connect_launcher.py"], capture_output=True, text=True)
        st.code(result.stdout)
        if result.returncode == 0:
            st.success("✅ Linking completed successfully!")
        else:
            st.error("❌ Linking failed.")
            st.code(result.stderr)
