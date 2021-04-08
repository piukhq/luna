import logging

from time import sleep

import falcon

from falcon.status_codes import HTTP_500

from app.settings import DEFAULT_FAILED_RESPONSES, DEFAULT_TIMEOUT_WAIT, cache


class PolarisEnrolCallback:
    logger = logging.getLogger("Polaris")

    @staticmethod
    def _get_secondary_param(route: str, default_value: int, max_val: int, min_val: int) -> int:
        try:
            param = int(route.split("-")[1])

        except (ValueError, IndexError):
            param = default_value
        else:
            if not min_val <= param < max_val:
                param = default_value

        return param

    @staticmethod
    def _get_cached_retries(key: str, value: int) -> int:
        retries = cache.get(key, int)

        if retries is not None:
            if retries < 1:
                cache.delete(key)
            else:
                cache.set(key, retries - 1)
        else:
            cache.set(key, value - 1)
            retries = value

        return retries

    def on_post(self, req: falcon.Request, resp: falcon.Response, route: str) -> None:
        if "timeout" in route:
            wait_time = self._get_secondary_param(route, DEFAULT_TIMEOUT_WAIT, 600, 0)
            self.logger.info(f"received request for timed out callback, waiting for {wait_time} seconds.")
            sleep(wait_time)
            resp.media = {"success": f"test callback timeout, waited for {wait_time} seconds."}

        elif "retry" in route:
            req_retries = self._get_secondary_param(route, DEFAULT_FAILED_RESPONSES, 5, 1)
            try:
                uid = req.media["UUID"]
            except KeyError:
                self.logger.error("callback payload missing UUID.")
                raise falcon.HTTPError(status=falcon.HTTP_422, description="callback payload missing value: UUID.")
            else:
                retries = self._get_cached_retries(uid, req_retries)

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
