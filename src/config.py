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
CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Raw Files
RAW_IMSDB_MOV_FILE_PATH = os.path.join(CWD, "data", "raw", "imsdb_movies.csv")
RAW_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    CWD, "data", "raw", "imsdb_movie_scripts.csv"
)

# Processed Files
PRO_IMDB_MOV_ROL_FILE_PATH = os.path.join(
    CWD, "data", "processed", "imdb_movie_roles.csv"
)
PRO_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    CWD, "data", "processed", "imsdb_movie_scripts_roles.csv"
)
PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    CWD, "data", "processed", "imdb_imsdb_movie_scripts.csv"
)

# Flask Environment
FASTAPI_ENV = os.getenv("FASTAPI_ENV")

# File Paths
VOCABULARY_FILE_PATH = os.path.join(CWD, "files", "vocabulary.csv")
TERM_DOC_FREQ_FILE_PATH = os.path.join(CWD, "files", "term_freq_map.csv")
