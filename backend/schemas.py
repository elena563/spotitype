from marshmallow import Schema, fields

class PlaylistFormSchema(Schema):
    form_type = fields.String(required=True)
    playlistField = fields.String(required=True)

class SongsFormSchema(Schema):
    form_type = fields.String(required=True)
    song1 = fields.String(required=True)
    song2 = fields.String(required=True)
    song3 = fields.String(required=True)
    song4 = fields.String(required=True)
    song5 = fields.String(required=True)