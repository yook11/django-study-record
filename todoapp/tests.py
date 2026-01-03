from django.test import TestCase
from .models import Todo

class TodoModelTests(TestCase):
    def test_is_empty(self):
        """最初はデータが空であることをテスト"""
        saved_todos = Todo.objects.all()
        self.assertEqual(saved_todos.count(), 0)

    def test_create_todo(self):
        """ToDoが正しく作成・保存できるかテスト"""
        # 1. データの作成（ロボットに命令）
        todo = Todo.objects.create(title="テストタスク", memo="これはテストです")

        # 2. 確認（ロボットにチェックさせる）
        # データベースの中身を全部持ってくる
        saved_todos = Todo.objects.all()
        
        # データが「1個」になっているはずだよね？
        self.assertEqual(saved_todos.count(), 1)
        
        # 保存されたデータのタイトルは「テストタスク」のはずだよね？
        actual_todo = saved_todos[0]
        self.assertEqual(actual_todo.title, "テストタスク")
