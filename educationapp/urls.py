from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='educationapp/orm_index.html'), name='orm_index'),
    path('student_list/', views.get_all_student, name='student_list'),
    path('student/<int:id>/', views.get_student_by_id, name='student_detail'),
    path('students/', views.filter_students, name='students_where'),
    path('students_with_profiles/', views.student_with_profile_list, name='students_join_profile'),
    path('class_students/', views.class_students, name='students_by_class'),
]