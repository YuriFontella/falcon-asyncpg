import falcon

from src.hooks.secure import secure
from src.storage.limits import limiter

from asyncpg import Pool

@falcon.before(secure)
class User:
    async def on_get(self, req, resp):
        try:
            pool: Pool = req.scope['state']['pool']

            async with pool.acquire() as conn:
                records = await conn.fetchrow("select name from users limit 1")
            
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        else:
            resp.media = dict(records)

    @limiter.limit()
    async def on_post(self, req, resp):
        pass
        try:
            pool: Pool = req.scope['state']['pool']

            data = await req.media
            query = """
              insert into users (name, group_id)
              values 
                ($1, $2) on conflict (name) do
              update
              set
                name = excluded.name
              returning id
            """

            async with pool.acquire() as conn:
                name = data['name']
                group_id = int(data['group_id'])

                record = await conn.fetchrow(query, name, group_id)

        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        else:
            resp.media = record['id']
