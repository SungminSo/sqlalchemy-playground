# sqlite3
# import os
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATABASE = {"engine": f"sqlite:///{BASE_DIR}/memory.db", "echo": False}


# postgresql
DATABASE = {"engine": "postgresql+psycopg2://postgres:password@localhost:5432/playground", "echo": True}
