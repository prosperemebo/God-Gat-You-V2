import os
import requests
from db import db
from app import create_app
from dotenv import load_dotenv
from models import LikeModel
from sqlalchemy.exc import IntegrityError

load_dotenv()

likes_url = os.getenv("LEGACY_LIKES_ENDPOINT", "https://likes.com")

database_name = os.getenv("POSTGRES_DB", "ggy_db")
database_user = os.getenv("POSTGRES_USER", "ggy_user")
database_password = os.getenv("POSTGRES_PASSWORD", "ggy_password")
database_host = os.getenv("POSTGRES_HOST", "localhost")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}?sslmode=disable"

app = create_app(database_url)


def fetch_likes(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        response.raise_for_status()


def store_likes(data):
    for item in data:
        like = LikeModel(
            user_id=item["user_id"],
            wallpaper_id=item["post_id"],
        )

        db.session.add(like)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"User {like.user_id} already liked wallpaper {like.wallpaper_id}.")


def main():
    with app.app_context():
        likes_data = fetch_likes(likes_url)
        store_likes(likes_data)

    print("Likes have been fetched and stored in the database successfully.")


if __name__ == "__main__":
    main()
