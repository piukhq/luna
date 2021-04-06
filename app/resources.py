import logging

from time import sleep

import falcon

from app.settings import DEFAULT_FAILED_RESPONSES, DEFAULT_TIMEOUT_WAIT

cache: dict = {}


class PolarisEnrolCallback:
    logger = logging.getLogger("Polaris")

    def on_post(self, req: falcon.Request, resp: falcon.Response, route: str) -> None:
        global cache

        if "timeout" in route:
            try:
                wait_time = int(route.split("-")[1])

            except (ValueError, IndexError):
                wait_time = DEFAULT_TIMEOUT_WAIT
            else:
                if 600 < wait_time <= 0:
                    wait_time = DEFAULT_TIMEOUT_WAIT

            self.logger.info(f"received request for timed out callback, waiting for {wait_time} seconds.")
            sleep(wait_time)
            resp.media = {"success": f"test callback timeout, waited for {wait_time} seconds."}

        elif "retry" in route:
            try:
                retries = int(route.split("-")[1])

            except (ValueError, IndexError):
                retries = DEFAULT_FAILED_RESPONSES
            else:
                if 5 < retries < 1:
                    retries = DEFAULT_FAILED_RESPONSES

            try:
                uid = req.media["UUID"]
            except KeyError as e:
                self.logger.exception("callback payload missing UUID.", exc_info=e)
            else:
                if uid in cache:
                    retries = cache[uid]
                    if retries < 1:
                        del cache[uid]
                    else:
                        cache[uid] = cache[uid] - 1
                else:
                    cache[uid] = retries - 1

                if retries < 1:
                    resp.status = falcon.HTTP_200
                    resp.media = {"success": "test callback retry, successful retry"}
                else:
                    resp.status = falcon.HTTP_500
                    resp.media = {"error": f"test callback retry, retries left before success {retries}"}

        elif route == "error":
            self.logger.info("received request for failed callback.")
            resp.status = falcon.HTTP_500
            resp.media = {"error": "test callback error."}

        else:
            self.logger.info("received request for successful callback.")
            resp.media = {"success": "test callback success"}
