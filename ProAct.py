import streamlit as st
import subprocess
import psutil
from UI import UI

def is_streamlit_running():
    """检查是否有正在运行的 Streamlit 实例"""
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'streamlit' in (process.info['name'] or '') or \
        any('streamlit' in cmd for cmd in (process.info['cmdline'] or [])):
            return True
    return False

if __name__ == "__main__":

    UI().render()
    
    if not is_streamlit_running():
        subprocess.run(["streamlit", "run", "ProAct.py"])
    else:
        print("Streamlit 已经在运行中，不需要重复启动！")