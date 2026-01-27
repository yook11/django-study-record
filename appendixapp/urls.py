from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("api/samples", views.SampleViewSet)

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="appendixapp/extends_index.html"),
        name="extends_index",
    ),
    path("one/", TemplateView.as_view(template_name="appendixapp/one.html"), name="extends_one"),
    path("two/", TemplateView.as_view(template_name="appendixapp/two.html"), name="extends_two"),
    path("samples/", views.sample_list, name="sample_list"),
    path("samples/<int:id>/", views.sample_detail, name="sample_detail"),
    path("samples/create/", views.sample_create, name="sample_create"),
    path("paginator/", views.samples_paginator, name="samples_paginator"),
    path("", include(router.urls)),
]
