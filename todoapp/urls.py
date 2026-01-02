from django.urls import path
from . import views

# todoapp/urls.py
urlpatterns = [
    # ① まず一覧を表示する（ここにアクセスしてボタンを押す）
    path('list/', views.TodoListView.as_view(), name='todo_list'),

    # ② ボタンを押した後に飛んでくる詳細ページ
    path('<int:pk>/', views.TodoDetailView.as_view(), name='todo_detail'),

    path('new/', views.TodoCreateView.as_view(), name='todo_create'),

    path('<int:pk>/edit/', views.TodoupdateView.as_view(), name='todo_update'),

    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo_delete'),
]