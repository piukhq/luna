import falcon

from luna.urls import urlpatterns


def create_app() -> falcon.App:
    app = falcon.App()
    app.req_options.strip_url_path_trailing_slash = True
    for uri_template, resource in urlpatterns:
        app.add_route(uri_template, resource)
    return app
