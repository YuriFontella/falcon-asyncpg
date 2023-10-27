import configparser
import os
import asyncpg

config = configparser.ConfigParser()
env = os.environ.get('ENV', 'development')
if env:
    config.read('config.ini')

class Pool:
    async def process_startup(self, scope, event):
        try:
            pool = await asyncpg.create_pool(dsn=config.get(env, 'DSN'), min_size=2, max_size=10)
            scope['state']['pool'] = pool
        except Exception as e:
            raise RuntimeError(f"Failed to create a database connection pool: {e}")

    async def process_shutdown(self, scope, event):
        pool = scope['state']['pool']
        if pool:
            await pool.close()
