from django.shortcuts import redirect
from django.urls import path

from . import views

# todoapp/urls.py
urlpatterns = [
    path("", lambda request: redirect("menu"), name="home"),
    # ① まず一覧を表示する（ここにアクセスしてボタンを押す）
    path("list/", views.TodoListView.as_view(), name="todo_list"),
    # ② ボタンを押した後に飛んでくる詳細ページ
    path("<int:pk>/", views.TodoDetailView.as_view(), name="todo_detail"),
    path("new/", views.TodoCreateView.as_view(), name="todo_create"),
    path("<int:pk>/edit/", views.TodoUpdateView.as_view(), name="todo_update"),
    path("<int:pk>/delete/", views.TodoDeleteView.as_view(), name="todo_delete"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("analytics/", views.TodoAnalyticsView.as_view(), name="todo_analytics"),
]
