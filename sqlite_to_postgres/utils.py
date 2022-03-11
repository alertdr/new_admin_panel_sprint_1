import uuid
from datetime import datetime

from dateutil import parser


def ISO_parse(created: str, modified: str) -> (datetime, datetime):
    return parser.parse(created), parser.parse(modified)


def multiple_uuid_parse(*args: str):
    return (uuid.UUID(i) for i in args)


def cast_types(data_id, created, modified):
    if not isinstance(data_id, uuid.UUID):
        data_id = uuid.UUID(data_id)

    if all([not isinstance(created, datetime), not isinstance(modified, datetime)]):
        created, modified = ISO_parse(created, modified)

    return data_id, created, modified
