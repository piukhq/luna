from collections import namedtuple

from app import healthz, resources
from app.settings import URL_PREFIX

URL = namedtuple("URL", ["uri_template", "resource"], defaults=[None, None])

urlpatterns = [
    URL(URL_PREFIX + "/enrol/callback/{route}", resources.PolarisEnrolCallback()),
    URL(URL_PREFIX + "/metadata/identity/oauth2/token", resources.PolarisCallbackOauth2Token()),
    URL(URL_PREFIX + "/bpl/retailers/{retailer_slug}/active-campaign-slugs", resources.ActiveCampaignSlugs()),
    URL("/livez", healthz.Livez()),
    URL("/readyz", healthz.Readyz()),
]
