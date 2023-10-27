import decimal
import orjson

from falcon import media
from functools import partial

def default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

json_handler = media.JSONHandler(
    dumps=partial(orjson.dumps, default=default),
    loads=orjson.loads
)

extra_handlers = {
    'application/json': json_handler
}
