import os
import requests
import shortuuid
from db import db
from app import create_app
from slugify import slugify
from datetime import datetime
from dotenv import load_dotenv
from models import WallpaperModel
from sqlalchemy.exc import IntegrityError

load_dotenv()

wallpapers_url = os.getenv("LEGACY_WALLPAPERS_ENDPOINT", "https://wallpapers.com")
database_name = os.getenv("POSTGRES_DB", "ggy_db")
database_user = os.getenv("POSTGRES_USER", "ggy_user")
database_password = os.getenv("POSTGRES_PASSWORD", "ggy_password")
database_host = os.getenv("POSTGRES_HOST", "localhost")
database_url = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}?sslmode=disable"

app = create_app(database_url)


def fetch_wallpapers(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        response.raise_for_status()


def store_wallpapers(data):
    for item in data:
        name = item["wallpaper_name"]

        slug = slugify(name.lower())
        existing_wallpaper = WallpaperModel.query.filter_by(slug=slug).first()

        if existing_wallpaper:
            slug = f"{slug}-{shortuuid.ShortUUID().random(length=5)}"

        wallpaper = WallpaperModel(
            id=item["paper_id"],
            name=name,
            slug=slug,
            thumbnail="wallpaper" + item["thumbnail"],
            mobile=item["mobile"],
            desktop=item["desktop"],
            tablet=item["tablet"],
            downloads=item["downloads"],
            description=item["body"],
        )

        db.session.add(wallpaper)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Wallpaper {wallpaper.name} already exists in the database.")


def main():
    with app.app_context():
        wallpaper_data = fetch_wallpapers(wallpapers_url)
        store_wallpapers(wallpaper_data)

    print("Wallpapers have been fetched and stored in the database successfully.")


if __name__ == "__main__":
    main()
