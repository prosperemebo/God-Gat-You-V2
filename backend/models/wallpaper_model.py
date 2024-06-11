from db import db

class WallpaperModel(db.Model):
    __tablename__ = "wallpapers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))