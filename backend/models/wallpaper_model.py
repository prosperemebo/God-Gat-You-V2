import uuid
from db import db
from .like_model import LikeModel
from sqlalchemy.ext.hybrid import hybrid_property


class WallpaperModel(db.Model):
    __tablename__ = "wallpapers"

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text())
    thumbnail = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(255))
    desktop = db.Column(db.String(255))
    tablet = db.Column(db.String(255))
    downloads = db.Column(db.Integer(), default=0)
    is_public = db.Column(
        db.Boolean(), default=True
    )  # Wallpaper is listed and publicaly accessible
    is_private = db.Column(
        db.Boolean(), default=False
    )  # Wallpaper is only accessible to the user
    publish_date = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )  # Date for wallpaper to be listed
    likes = db.relationship(
        "LikeModel", back_populates="wallpaper", lazy="dynamic", cascade="all, delete"
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, id=None, **kwargs):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)

    @hybrid_property
    def likes_count(self):
        return self.likes.count()

    @likes_count.expression
    def likes_count(cls):
        return (
            db.select([db.func.count(LikeModel.id)])
            .where(LikeModel.wallpaper_id == cls.id)
            .label("likes_count")
        )

    def update(self, **kwargs):
        restricted_fields = [self.id, self.created_at, self.updated_at]

        for key, value in kwargs.items():
            if key in restricted_fields:
                continue

            setattr(self, key, value)
