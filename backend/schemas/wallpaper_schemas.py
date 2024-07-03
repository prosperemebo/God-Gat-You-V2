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
    likes_count = fields.Int(dump_only=True)
    is_public = fields.Bool()
    is_private = fields.Bool()
    publish_date = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class WallpaperSchema(_WallpaperSchema):
    pass


class AllWallpapersSchema(ResponseSchema):
    data = fields.List(fields.Nested(WallpaperSchema))
    page = fields.Int()
    page_size = fields.Int()
    total_count = fields.Int()
    total_pages = fields.Int()



class WallpaperFilesSchema(Schema):
    thumbnail = fields.Raw(type="file", required=True)
    mobile = fields.Raw(type="file", required=False)
    desktop = fields.Raw(type="file", required=False)
    tablet = fields.Raw(type="file", required=False)
