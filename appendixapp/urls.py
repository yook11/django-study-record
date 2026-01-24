from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="appendixapp/extends_index.html"), name="extends_index"),
    path('one/', TemplateView.as_view(template_name="appendixapp/extends_one.html"), name="extends_one"),
    path('two/', TemplateView.as_view(template_name="appendixapp/extends_two.html"), name="extends_two"),
]