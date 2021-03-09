"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import print_function
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Custom admin header
admin.site.site_header = "OpenFisca Django-API Administration"

urlpatterns = [
    path("entities/", include(("entities.urls", "entities"), namespace="entities")),
    path("variables/", include(("variables.urls", "variables"), namespace="variables")),
    url(r"^admin/", admin.site.urls),
    # SWAGGER PATHS
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("plots/", include(("plots.urls", "plots"), namespace="plots"))
]

# Host the static from uWSGI
if settings.IS_WSGI:
    print("uWSGI mode, adding static file patterns")
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()

# Add debug toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
