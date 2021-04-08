import falcon

from app.settings import USE_REDIS_CACHE, cache


class Livez:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.media = {}


class Readyz:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        resp.media = {}

        if USE_REDIS_CACHE:
            try:
                cache.set("readyz", "true")
                cache.get("readyz")
                cache.delete("readyz")
            except Exception as e:
                resp.media = {"redis": f"failed to connect to redis due to error: {repr(e)}"}
                resp.status = falcon.HTTP_500
