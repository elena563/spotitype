from marshmallow import Schema, fields, validate

class PlaylistFormSchema(Schema):
    form_type = fields.String(required=True, validate=validate.Length(min=1))
    playlistField = fields.String(required=True, validate=validate.Length(min=1))

class SongsFormSchema(Schema):
    form_type = fields.String(required=True, validate=validate.Length(min=1))
    song1 = fields.String(required=True, validate=validate.Length(min=1))
    song2 = fields.String(required=True, validate=validate.Length(min=1))
    song3 = fields.String(required=True, validate=validate.Length(min=1))
    song4 = fields.String(required=True, validate=validate.Length(min=1))
    song5 = fields.String(required=True, validate=validate.Length(min=1))