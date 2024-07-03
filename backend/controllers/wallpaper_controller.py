import os
import boto3
from sqlalchemy import desc, or_
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
    WallpaperFilesSchema,
)
from utils import allowed_file_or_abort
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

        pagination = WallpaperModel.query.order_by(
            desc(WallpaperModel.created_at)
        ).paginate(
            page=page,
            per_page=page_size,
            count=True,
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

    @blueprint.arguments(WallpaperSchema, location="form")
    @blueprint.arguments(WallpaperFilesSchema, location="files")
    @blueprint.response(201, WallpaperSchema)
    def post(self, form_data, files_data):
        thumbnail_file = (
            request.files["thumbnail"] if "thumbnail" in request.files else None
        )
        desktop_file = request.files["desktop"] if "desktop" in request.files else None
        mobile_file = request.files["mobile"] if "mobile" in request.files else None
        tablet_file = request.files["tablet"] if "tablet" in request.files else None

        slug = slugify(
            form_data["name"].lower() if "name" in form_data else "wallpaper",
        )
        existing_wallpaper = WallpaperModel.query.filter_by(slug=slug).first()

        if existing_wallpaper:
            slug = f"{slug}-{shortuuid.ShortUUID().random(length=5)}"

        files_data = []

        if thumbnail_file == None:
            abort(400, message="Thumbnail is required")

        files_data.append(allowed_file_or_abort(thumbnail_file, slug, "thumbnail"))

        if desktop_file is not None:
            files_data.append(allowed_file_or_abort(desktop_file, slug, "desktop"))

        if mobile_file is not None:
            files_data.append(allowed_file_or_abort(mobile_file, slug, "mobile"))

        if tablet_file is not None:
            files_data.append(allowed_file_or_abort(tablet_file, slug, "tablet"))

        boto_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_secret_key,
            region_name=region_name,
        )

        s3_client = boto_session.resource("s3")

        for file_data in files_data:
            s3_client.Bucket(bucket_name).upload_fileobj(
                file_data["file"],
                path_prefix + file_data["filename"],
            )

            form_data[file_data["type"]] = file_data["filename"]

        form_data["slug"] = slug

        wallpaper = WallpaperModel(**form_data)
        db.session.add(wallpaper)

        try:
            db.session.commit()
        except IntegrityError:
            for file_data in files_data:
                s3_client.Object(
                    bucket_name, path_prefix + file_data["filename"]
                ).delete()

            db.session.rollback()
            abort(400, message="Wallpaper already exists")

        return wallpaper


@blueprint.route("/<int:wallpaper_id>")
class Wallpaper(MethodView):
    @blueprint.response(200, WallpaperSchema)
    def get(self, wallpaper_id):
        return WallpaperModel.query.filter(
            or_(WallpaperModel.id == wallpaper_id, WallpaperModel.slug == wallpaper_id)
        ).first_or_404()

    @blueprint.arguments(WallpaperFilesSchema, location="files")
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
