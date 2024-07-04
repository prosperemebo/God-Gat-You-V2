import uuid
from db import db


class LikeModel(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey("users.id"), nullable=False)
    wallpaper_id = db.Column(db.String(100), db.ForeignKey("wallpapers.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="likes")
    wallpaper = db.relationship("WallpaperModel", back_populates="likes")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'wallpaper_id', name='unique_user_wallpaper_like'),
    )

    def __init__(self, id=None, **kwargs):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

        for key, value in kwargs.items():
            setattr(self, key, value)
