from collections import namedtuple

from app import resources

URL = namedtuple("URL", ["uri_template", "resource"], defaults=[None, None])

urlpatterns = [
    URL("/enrol/callback/{route}", resources.PolarisEnrolCallback()),
]
