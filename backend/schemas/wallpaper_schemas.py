from marshmallow import Schema, fields

class _WallpaperSchema(Schema):
	id = fields.Int()
	name = fields.Str()
	slug = fields.Str()
	description = fields.Str()
 
class WallpaperSchema(_WallpaperSchema):
	pass