from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from db import db
from models import WallpaperModel
from schemas import WallpaperSchema

blueprint = Blueprint(
    "Wallpapers", __name__, description="Wallpapers related operations"
)


@blueprint.route("/api/v1/wallpapers")
class Wallpapers(MethodView):
    @blueprint.response(200, WallpaperSchema(many=True))
    def get(self):
        return WallpaperModel.query.all()

    @blueprint.arguments(WallpaperSchema)
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


@blueprint.route("/api/v1/wallpapers/<int:wallpaper_id>")
class Wallpaper(MethodView):
    @blueprint.response(200, WallpaperSchema(many=True))
    def get(self, wallpaper_id):
        return WallpaperModel.query.get_or_404(wallpaper_id)

    @blueprint.arguments(WallpaperSchema)
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
