from src.extract import extract
from src.transform import transform
from src.model import model
import sys
from pathlib import Path

def launch_streamlit_app():
    from streamlit.web import cli as stcli
    app_path = "app/streamlit_app.py"
    sys.argv = ["streamlit", "run", app_path]
    stcli.main()

def main():
    extract()
    transform()
    model()

    launch_streamlit_app()

if __name__ == "__main__":
    main()