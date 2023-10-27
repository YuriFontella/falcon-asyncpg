import configparser
import os
import asyncpg

config = configparser.ConfigParser()
env = os.environ.get('ENV', 'development')
if env:
    config.read('config.ini')

class Pool:
    def __init__(self):
        self.pool = None

    async def process_startup(self, scope, event):
        try:
            self.pool = await asyncpg.create_pool(dsn=config.get(env, 'DSN'), min_size=2, max_size=4)
        except Exception as e:
            raise RuntimeError(f"Failed to create a database connection pool: {e}")

    async def process_shutdown(self, scope, event):
        if self.pool:
            await self.pool.close()

    async def process_request(self, req, resp):
        req.context.pool = self.pool
