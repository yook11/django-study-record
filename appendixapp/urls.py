from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="appendixapp/extends_index.html"), name="extends_index"),
    path('one/', TemplateView.as_view(template_name="appendixapp/one.html"), name="extends_one"),
    path('two/', TemplateView.as_view(template_name="appendixapp/two.html"), name="extends_two"),
    path('samples/', views.sample_list, name="sample_list"),
    path('samples/<int:id>/', views.sample_detail, name="sample_detail"),
    path('samples/create/', views.sample_create, name="sample_create"),
]