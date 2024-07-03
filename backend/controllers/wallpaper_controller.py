import os
import boto3
import shortuuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from db import db
from slugify import slugify
from models import WallpaperModel
from schemas import (
    WallpaperSchema,
    AllWallpapersSchema,
    CreateWallpaperSchema,
)
from utils.functions import is_file_allowed, allowed_file_or_abort
from flask import request

blueprint = Blueprint(
    "Wallpapers",
    __name__,
    description="Wallpapers related operations",
    url_prefix="/api/v1/wallpapers",
)

access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "")
access_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
region_name = os.getenv("AWS_REGION_NAME", "")
bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "")
path_prefix = os.getenv("AWS_UPLOAD_PATH_PREFIX", "")


@blueprint.route("/")
class Wallpapers(MethodView):
    @blueprint.response(200, AllWallpapersSchema)
    @blueprint.paginate()
    def get(self, pagination_parameters):
        page = pagination_parameters.page
        page_size = pagination_parameters.page_size

        pagination = WallpaperModel.query.paginate(
            page=page, per_page=page_size, count=True
        )
        wallpapers = pagination.items
        total_count = pagination.total
        total_pages = pagination.pages

        response = {
            "status": "success",
            "message": f"Found {len(wallpapers)} wallpapers",
            "data": wallpapers,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
            "total_pages": total_pages,
        }

        return response

    @blueprint.arguments(CreateWallpaperSchema, location="files")
    @blueprint.response(201, WallpaperSchema)
    def post(self, new_data):
        thumbnail_file = request.files.get("thumbnail", None)
        desktop_file = request.files.get("desktop", None)
        mobile_file = request.files.get("mobile", None)
        tablet_file = request.files.get("tablet", None)

        slug = slugify(new_data["name"])
        existing_wallpaper = WallpaperModel.query.filter_by(slug=slug).first()

        if existing_wallpaper:
            slug = f"{slug}-{shortuuid.ShortUUID().random(length=5)}"

        files_data = []

        if not thumbnail_file:
            abort(400, message="Thumbnail is required")

        if not is_file_allowed(thumbnail_file.filename):
            abort(400, message="Invalid thumbnail file type")
        else:
            filename = f"ggy-{slug}-thumbnail.{thumbnail_file.filename.rsplit('.', 1)[1].lower()}"
            file_data = {
                "file": thumbnail_file,
                "filename": filename,
            }

            files_data.append(file_data)

        files_data.append(
            allowed_file_or_abort(
                thumbnail_file, "Invalid thumbnail file type", slug, "thumbnail"
            )
        )
        files_data.append(
            allowed_file_or_abort(
                desktop_file, "Invalid desktop file type", slug, "desktop"
            )
        )
        files_data.append(
            allowed_file_or_abort(
                mobile_file, "Invalid mobile file type", slug, "mobile"
            )
        )
        files_data.append(
            allowed_file_or_abort(
                tablet_file, "Invalid tablet file type", slug, "tablet"
            )
        )

        boto_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_secret_key,
            region_name=region_name,
        )

        s3_client = boto_session.resource("s3")

        for file_data in files_data:
            s3_client.upload_file(
                file_data["file"],
                bucket_name,
                path_prefix + file_data["filename"],
            )

            new_data[file_data["type"]] = file_data["filename"]

        new_data["slug"] = slug

        wallpaper = WallpaperModel(**new_data)
        db.session.add(wallpaper)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Wallpaper already exists")

        return wallpaper


@blueprint.route("/<int:wallpaper_id>")
class Wallpaper(MethodView):
    @blueprint.response(200, WallpaperSchema)
    def get(self, wallpaper_id):
        return WallpaperModel.query.get_or_404(wallpaper_id)

    @blueprint.arguments(CreateWallpaperSchema, location="files")
    @blueprint.response(201, WallpaperSchema)
    def put(self, wallpaper_data, wallpaper_id):
        wallpaper = WallpaperModel.query.get_or_404(wallpaper_id)

        wallpaper.update(**wallpaper_data)
        db.session.commit()

        return wallpaper

    @blueprint.response(204)
    def delete(self, wallpaper_id):
        wallpaper = WallpaperModel.query.get_or_404(wallpaper_id)

        boto_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_secret_key,
            region_name=region_name,
        )

        s3_client = boto_session.resource("s3")

        files_to_delete = [
            wallpaper.thumbnail,
            wallpaper.desktop,
            wallpaper.mobile,
            wallpaper.tablet,
        ]

        for filename in files_to_delete:
            if filename:
                s3_client.Object(bucket_name, path_prefix + filename).delete()

        db.session.delete(wallpaper)
        db.session.commit()

        return None
