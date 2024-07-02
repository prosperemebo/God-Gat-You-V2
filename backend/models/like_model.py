from db import db


class LikeModel(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.UUID(), primary_key=True)
    user_id = db.Column(db.UUID(), db.ForeignKey("users.id"), nullable=False)
    wallpaper_id = db.Column(db.UUID(), db.ForeignKey("wallpapers.id"), nullable=False)
    user = db.relationship('UserModel', back_populates='likes')
    wallpaper = db.relationship('WallpaperModel', back_populates='likes')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
