from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from db import db
from models import WallpaperModel
from schemas import (
    WallpaperSchema,
    AllWallpapersSchema,
    WallpaperQuerySchema,
    CreateWallpaperSchema,
    ResponseSchema,
)
from flask import request

blueprint = Blueprint(
    "Wallpapers",
    __name__,
    description="Wallpapers related operations",
    url_prefix="/api/v1/wallpapers",
)


@blueprint.route("/")
class Wallpapers(MethodView):
    @blueprint.response(200, AllWallpapersSchema)
    @blueprint.paginate()
    def get(pagination_parameters):
        page = pagination_parameters.page
        page_size = pagination_parameters.page_size

        pagination = WallpaperModel.query.paginate(page=page, per_page=page_size, count=True)
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

        db.session.delete(wallpaper)
        db.session.commit()

        return None
