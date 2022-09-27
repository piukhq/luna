import falcon

from luna.settings import USE_REDIS_CACHE, cache


class Livez:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:  # pylint: disable=unused-argument
        resp.media = {}


class Readyz:
    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:  # pylint: disable=unused-argument
        resp.media = {}

        if USE_REDIS_CACHE:
            try:
                cache.set("readyz", "true")
                cache.get("readyz")
                cache.delete("readyz")
            except Exception as ex:  # pylint: disable=broad-except
                resp.media = {"redis": f"failed to connect to redis due to error: {repr(ex)}"}
                resp.status = falcon.HTTP_500
