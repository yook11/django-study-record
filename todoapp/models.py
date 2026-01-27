from django.contrib.auth.models import User
from django.db import models
from django_pandas.io import read_frame


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=30)

    memo = models.TextField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    @classmethod
    def get_completion_stats(cls):
        """完了済み、および未完了のタスクを集計して返す"""
        # 全てのタスクを取得
        todos = cls.objects.all()
        # 完了済みのタスク数をカウント
        completed = todos.filter(completed=True).count()
        # 未完了のタスクの数をカウント
        not_completed = todos.filter(completed=False).count()
        # 総タスク数
        total = completed + not_completed

        # 完了率を計算、タスクが０の時は０除算を避けてreturn0
        if total > 0:
            completion_rate = round((completed / total) * 100, 2)
        else:
            completion_rate = 0

        # 統計情報を辞書として返す
        return {
            "completed": completed,
            "not_completed": not_completed,
            "total": total,
            "completion_rate": completion_rate,
        }

    @classmethod
    def get_todos_dataframe(cls):
        """ToDoデータをpandasのdataframeに変換する"""

        # 全てのタスクを取得する(QuerySet)
        todos = cls.objects.all()

        # DjangoのQuerySetをpandasのDataFrameに変換
        return read_frame(todos)
