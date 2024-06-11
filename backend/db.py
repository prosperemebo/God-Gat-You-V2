import os
from flask_sqlalchemy import SQLAlchemy

database_name = os.getenv("DATABASE_NAME", "ggy_db")
database_user = os.getenv("DATABASE_USER", "ggy_user")
database_password = os.getenv("DATABASE_PASSWORD", "ggy_password")
database_host = os.getenv("DATABASE_HOST", "localhost")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}:5432/{database_name}?sslmode=disable"

db = SQLAlchemy()
