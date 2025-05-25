import os
from dotenv import load_dotenv

load_dotenv()

SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")
