import uuid
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    likes = db.relationship('LikeModel', back_populates='user', lazy='dynamic', cascade='all, delete')
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
