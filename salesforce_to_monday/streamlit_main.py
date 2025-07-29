import streamlit as st
import subprocess
import sys

st.title("📊 Salesforce ↔ Monday.com Sync Tool")

def run_command_live(command):
    placeholder = st.empty()
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    log = ""
    for line in process.stdout:
        log += line
        placeholder.code(log, language="bash")
    
    process.stdout.close()
    process.wait()
    
    if process.returncode == 0:
        st.success("✅ Operation completed successfully!")
    else:
        st.error("❌ Operation failed. Check the logs above.")

# 🔄 버튼 1: 아이템 동기화
if st.button("🔄 Sync Items from Salesforce"):
    st.info("Running item sync...")
    run_command_live([sys.executable, "main.py", "sync"])
