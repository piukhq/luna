import falcon


def create_app() -> falcon.App:
    from app import settings  # noqa for now no setting needed anywhere
    from app.urls import urlpatterns

    app = falcon.App()
    app.req_options.strip_url_path_trailing_slash = True
    for uri_template, resource in urlpatterns:
        app.add_route(uri_template, resource)
    return app
