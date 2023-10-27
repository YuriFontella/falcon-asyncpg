import falcon.asgi

from src.resources.user import User
from src.middlewares.auth import Auth
from src.storage.limits import Limiter
from src.storage.transform import extra_handlers
from config.database import Pool

app = falcon.asgi.App(middleware=[Auth(), Pool(), Limiter()])

app.resp_options.media_handlers.update(extra_handlers)
app.req_options.media_handlers.update(extra_handlers)

app.add_route('/users', User())
