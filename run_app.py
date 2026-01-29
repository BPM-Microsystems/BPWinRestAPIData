"""
Launcher script for DataPanel Streamlit application
This script properly launches Streamlit when packaged as an EXE
"""
import sys
import os
from streamlit.web import cli as stcli

if __name__ == '__main__':
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        application_path = sys._MEIPASS
    else:
        # Running as script
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Path to DataPanel.py
    script_path = os.path.join(application_path, 'DataPanel.py')
    
    # Set up arguments for streamlit
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false",
        "--server.port=8501",
        "--server.headless=true",
        "--browser.serverAddress=localhost",
        "--browser.gatherUsageStats=false",
    ]
    
    # Run streamlit
    sys.exit(stcli.main())
