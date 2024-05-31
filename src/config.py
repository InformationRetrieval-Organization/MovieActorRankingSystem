from datetime import datetime, time
import os
import sys

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# API Keys
# GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# URL´s
IMDB_URL = "https://www.imdb.com"
IMSDB_URL = "https://www.imsdb.com"

# File Paths
CWD = os.getcwd()
MOV_FILE_PATH = os.path.join(CWD, "files", "movie_details_no_scripted.csv")
MOV_SCR_FILE_PATH = os.path.join(CWD, "files", "movie_scripts.csv")
MOV_ROL_FILE_PATH = os.path.join(CWD, "files", "movie_roles.csv")

# Flask Environment
FASTAPI_ENV = os.getenv("FASTAPI_ENV")
