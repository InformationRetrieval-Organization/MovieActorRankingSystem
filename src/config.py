import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Flask Environment
FASTAPI_ENV = os.getenv("FASTAPI_ENV")

# General paths
CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_PATH = os.path.join(CWD, "files")
DATA_PATH = os.path.join(CWD, "data")

# File Paths
VOCABULARY_FILE_PATH = os.path.join(FILES_PATH, "vocabulary.csv")
TERM_DOC_FREQ_FILE_PATH = os.path.join(FILES_PATH, "term_freq_map.csv")


# ---------------------------- START DATA CRAWLING ----------------------------
# URL´s
IMDB_URL = "https://www.imdb.com"
IMSDB_URL = "https://www.imsdb.com"

# Raw Files
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
RAW_IMSDB_MOV_FILE_PATH = os.path.join(RAW_DATA_PATH, "imsdb_movies.csv")
RAW_IMSDB_MOV_SCR_FILE_PATH = os.path.join(RAW_DATA_PATH, "imsdb_movie_scripts.csv")

# Processed Files
PRO_DATA_PATH = os.path.join(DATA_PATH, "processed")
PRO_IMDB_MOV_ROL_FILE_PATH = os.path.join(PRO_DATA_PATH, "imdb_movie_roles.csv")
PRO_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    PRO_DATA_PATH, "imsdb_movie_scripts_roles.csv"
)
PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH = os.path.join(
    PRO_DATA_PATH, "imdb_imsdb_movie_scripts.csv"
)
# ---------------------------- END DATA CRAWLING ----------------------------
