from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    enrollment_date = models.DateField()

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=255)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name}のプロフィール"