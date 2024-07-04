import os
from venv import logger
import boto3
import shortuuid

from db import db
from flask import request
from slugify import slugify
from datetime import datetime
from sqlalchemy import asc, desc, or_
from models import WallpaperModel
from flask.views import MethodView
from utils import allowed_file_or_abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import Blueprint, abort

from schemas import (
    WallpaperSchema,
    AllWallpapersSchema,
    WallpaperFilesSchema,
    UpdateWallpaperFilesSchema,
    UpdateWallpaperSchema,
    SearchWallpaperSchema,
)

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
path_prefix = os.getenv("AWS_UPLOAD_PATH_PREFIX", "") + "wallpaper/"


@blueprint.route("/")
class Wallpapers(MethodView):
    @blueprint.response(200, AllWallpapersSchema)
    @blueprint.paginate(page=1, page_size=100)
    def get(self, pagination_parameters):
        page = pagination_parameters.page
        page_size = pagination_parameters.page_size

        sort_by = request.args.get("sort", "created_at")
        order = request.args.get("order", "desc")

        sort_order = desc

        if order == "asc":
            sort_order = asc

        if sort_by not in ["created_at", "likes_count", "downloads"]:
            sort_by = "created_at"

        sort_attr = getattr(WallpaperModel, sort_by)

        pagination = WallpaperModel.query.order_by(sort_order(sort_attr)).paginate(
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

    @blueprint.route("/search")
    @blueprint.arguments(SearchWallpaperSchema, location="query")
    @blueprint.response(200, AllWallpapersSchema)
    @blueprint.paginate(page=1, page_size=100)
    def search_wallpapers(self, pagination_parameters):
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
        trials = 0

        while existing_wallpaper:
            if trials == 0:
                current_year = str(datetime.now().year)
                slug = f"{slug}-{current_year}"

                trials += 1
            else:
                slug = f"{slug}-{shortuuid.ShortUUID().random(length=5)}"

            existing_wallpaper = WallpaperModel.query.filter_by(slug=slug).first()

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
            abort(400, message="A Wallpaper name already exists!")
        except SQLAlchemyError:
            abort(
                500, message="An error occurred while adding the item to the database."
            )

        return wallpaper


@blueprint.route("/<string:wallpaper_id>")
class Wallpaper(MethodView):
    @blueprint.response(200, WallpaperSchema)
    def get(self, wallpaper_id):
        return WallpaperModel.query.filter(
            or_(WallpaperModel.id == wallpaper_id, WallpaperModel.slug == wallpaper_id)
        ).first_or_404()

    @blueprint.get("/<string:wallpaper_id>/download")
    @blueprint.response(200, WallpaperSchema)
    def download(wallpaper_id):
        wallpaper = WallpaperModel.query.filter(
            or_(WallpaperModel.id == wallpaper_id, WallpaperModel.slug == wallpaper_id)
        ).first_or_404()

        wallpaper.downloads += 1

        db.session.commit()

        return wallpaper

    @blueprint.arguments(UpdateWallpaperSchema, location="form")
    @blueprint.arguments(UpdateWallpaperFilesSchema, location="files")
    @blueprint.response(201, WallpaperSchema)
    def put(self, wallpaper_data, wallpaper_files, wallpaper_id):
        thumbnail_file = (
            request.files["thumbnail"] if "thumbnail" in request.files else None
        )
        desktop_file = request.files["desktop"] if "desktop" in request.files else None
        mobile_file = request.files["mobile"] if "mobile" in request.files else None
        tablet_file = request.files["tablet"] if "tablet" in request.files else None

        wallpaper = WallpaperModel.query.get_or_404(wallpaper_id)

        wallpaper.update(**wallpaper_data)

        if "name" in wallpaper_data:
            slug = slugify(
                (wallpaper_data["name"].lower()),
            )
            existing_wallpaper = WallpaperModel.query.filter_by(slug=slug).first()

            if existing_wallpaper:
                slug = f"{slug}-{shortuuid.ShortUUID().random(length=5)}"

            wallpaper.slug = slug

        unique_slug_for_files = wallpaper.slug + shortuuid.ShortUUID().random(length=5)
        files_data = []
        files_to_delete = []

        if thumbnail_file is not None:
            files_data.append(
                allowed_file_or_abort(
                    thumbnail_file, unique_slug_for_files, "thumbnail"
                )
            )
            files_to_delete.append(wallpaper.thumbnail)

        if desktop_file is not None:
            files_data.append(
                allowed_file_or_abort(desktop_file, unique_slug_for_files, "desktop")
            )
            files_to_delete.append(wallpaper.desktop)

        if mobile_file is not None:
            files_data.append(
                allowed_file_or_abort(mobile_file, unique_slug_for_files, "mobile")
            )
            files_to_delete.append(wallpaper.mobile)

        if tablet_file is not None:
            files_data.append(
                allowed_file_or_abort(tablet_file, unique_slug_for_files, "tablet")
            )
            files_to_delete.append(wallpaper.tablet)

        boto_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_secret_key,
            region_name=region_name,
        )

        s3_client = boto_session.client("s3")

        try:
            for file_data in files_data:
                s3_client.upload_fileobj(
                    file_data["file"], bucket_name, path_prefix + file_data["filename"]
                )
                setattr(wallpaper, file_data["type"], file_data["filename"])

            db.session.commit()

            for filename in files_to_delete:
                if filename:
                    s3_client.delete_object(
                        Bucket=bucket_name, Key=path_prefix + filename
                    )

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error committing to database: {str(e)}")
            abort(
                500, description="An internal error occurred. Please try again later."
            )

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error uploading to S3: {str(e)}")
            abort(
                500,
                description="An error occurred while uploading files. Please try again later.",
            )

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
