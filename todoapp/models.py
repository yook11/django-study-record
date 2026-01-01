from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=30)

    memo = models.TextField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


# Create your models here.
