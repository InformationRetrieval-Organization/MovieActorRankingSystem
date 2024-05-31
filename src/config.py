import os

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

# Raw Files
RAW_IMSDB_MOV_FILE_PATH = os.path.join(CWD, "data", "raw", "imsdb_movies.csv")
RAW_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    CWD, "data", "raw", "imsdb_movie_scripts.csv"
)

# Processed Files
PRO_MOV_ROL_FILE_PATH = os.path.join(CWD, "data", "processed", "movie_roles.csv")
PRO_MOV_SCR_FILE_PATH = os.path.join(
    CWD, "data", "processed", "movie_scripts_roles.csv"
)

# Flask Environment
FASTAPI_ENV = os.getenv("FASTAPI_ENV")
