import os
from flask_sqlalchemy import SQLAlchemy

database_name = os.getenv("POSTGRES_DB", "ggy_db")
database_user = os.getenv("POSTGRES_USER", "ggy_user")
database_password = os.getenv("POSTGRES_PASSWORD", "ggy_password")
database_host = os.getenv("POSTGRES_HOST", "localhost")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}?sslmode=disable"

db = SQLAlchemy()
