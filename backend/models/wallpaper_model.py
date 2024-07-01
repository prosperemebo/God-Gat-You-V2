from db import db

class WallpaperModel(db.Model):
    __tablename__ = "wallpapers"
    
    id = db.Column(db.UUID(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text())
    thumbnail = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(255))
    desktop = db.Column(db.String(255))
    tablet = db.Column(db.String(255))
    downloads = db.Column(db.Integer(), default=0)
    likes = db.Column(db.Integer(), default=0)
    is_public = db.Column(db.Boolean(), default=True) # Wallpaper is listed and publicaly accessible
    is_private = db.Column(db.Boolean(), default=False) # Wallpaper is only accessible to the user
    publish_date = db.Column(db.DateTime(timezone=False), default=True) # Date for wallpaper to be listed