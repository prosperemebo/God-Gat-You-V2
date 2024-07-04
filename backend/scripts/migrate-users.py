import os
import requests
from dotenv import load_dotenv
import shortuuid
from sqlalchemy.exc import IntegrityError
from app import create_app
from db import db
from models import UserModel

load_dotenv()

users_url = os.getenv("LEGACY_USERS_ENDPOINT", "https://users.com")
database_name = os.getenv("POSTGRES_DB", "ggy_db")
database_user = os.getenv("POSTGRES_USER", "ggy_user")
database_password = os.getenv("POSTGRES_PASSWORD", "ggy_password")
database_host = os.getenv("POSTGRES_HOST", "localhost")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}?sslmode=disable"

app = create_app(database_url)


def fetch_users(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        response.raise_for_status()


def store_users(data):
    for item in data:
        names = item["username"].split(" ")
        first_name = names[0] if names[0] else ""
        last_name = names[0] if names[0] else ""

        email = (
            first_name.lower()
            + "."
            + last_name.lower()
            + "."
            + shortuuid.ShortUUID().random(length=5)
            + "@godgatyou.com"
        )

        user = UserModel(
            id=item["user_id"],
            first_name=first_name,
            last_name=last_name,
            email=email,
            password="password12345",
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"User {user.first_name} already exists in the database.")


def main():
    with app.app_context():
        users_data = fetch_users(users_url)
        store_users(users_data)

    print("Users have been fetched and stored in the database successfully.")


if __name__ == "__main__":
    main()
