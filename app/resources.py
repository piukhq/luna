import logging

from datetime import datetime, timedelta
from time import sleep

import falcon

from app.settings import DEFAULT_FAILED_RESPONSES, DEFAULT_TIMEOUT_WAIT, cache

logger = logging.getLogger("Polaris")


class PolarisEnrolCallback:
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
        key = "polaris-enrol-retry:%s" % key

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
            logger.info(f"received request for timed out callback, waiting for {wait_time} seconds.")
            sleep(wait_time)
            resp.media = {"success": f"test callback timeout, waited for {wait_time} seconds."}

        elif "retry" in route:
            req_retries = self._get_secondary_param(route, DEFAULT_FAILED_RESPONSES, 5, 1)
            try:
                uid = req.media["UUID"]
            except KeyError:
                logger.error("callback payload missing UUID.")
                raise falcon.HTTPError(status=falcon.HTTP_422, description="callback payload missing value: UUID.")
            else:
                retries = self._get_cached_retries(uid, req_retries)

                if retries < 1:
                    resp.status = falcon.HTTP_200
                    resp.media = {"success": "test callback retry, successful retry"}
                else:
                    resp.status = falcon.HTTP_500
                    resp.media = {"error": f"test callback retry, retries left before success {retries}"}

        elif "error" in route:
            logger.info("received request for failed callback.")
            default_http_error_status = 500
            custom_status = self._get_secondary_param(route, default_http_error_status, 600, 200)
            try:
                response_status = getattr(falcon, f"HTTP_{custom_status}")
            except AttributeError:
                logger.warning(
                    f"invalid requested HTTP status code: {custom_status} for url path: {route}. "
                    f"defaulting to HTTP status code: {default_http_error_status}."
                )
                response_status = getattr(falcon, f"HTTP_{default_http_error_status}")

            resp.status = response_status
            resp.media = {"error": "test callback error."}

        else:
            logger.info("received request for successful callback.")
            resp.media = {"success": "test callback success"}


class PolarisCallbackOauth2Token:
    token_life = 86400  # 24 hours

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        now = datetime.now()
        shift = timedelta(seconds=self.token_life)
        resp.media = {
            "access_token": "luna-mock-token",
            "refresh_token": "",
            "expires_in": str(self.token_life),
            "expires_on": int((now + shift).timestamp()),
            "not_before": int(now.timestamp()),
            "resource": req.params.get("resource", "N/A"),
            "token_type": "Bearer",
        }
        logger.info("recevied request for a callback Oauth2 token.")
