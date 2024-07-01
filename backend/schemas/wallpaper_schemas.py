from marshmallow import Schema, fields
from .response_schema import ResponseSchema


class _WallpaperSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    slug = fields.Str()
    description = fields.Str()
    thumbnail = fields.Str()
    mobile = fields.Str()
    desktop = fields.Str()
    tablet = fields.Str()
    downloads = fields.Int(dump_only=True)
    likes = fields.Int(dump_only=True)


class WallpaperSchema(_WallpaperSchema):
    pass


class AllWallpapersSchema(ResponseSchema):
    data = fields.List(fields.Nested(WallpaperSchema))
    page = fields.Int()
    page_size = fields.Int()
    total_count = fields.Int()
    total_pages = fields.Int()


class CreateWallpaperSchema(_WallpaperSchema):
    thumbnail = fields.Raw(type="file", required=True)
    mobile = fields.Raw(type="file", required=True)
    desktop = fields.Raw(type="file", required=True)
    tablet = fields.Raw(type="file", required=True)


class WallpaperQuerySchema(Schema):
    page = fields.Int()
    page_size = fields.Int()
