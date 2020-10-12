from app import ma

from marshmallow import fields


class PaginationSchema(ma.Schema):

    offset = fields.Integer(dump_to='offset', dump_only=True)
    limit = fields.Integer(dump_to='limit', dump_only=True)
    total = fields.Integer(dump_to='total', dump_only=True)
