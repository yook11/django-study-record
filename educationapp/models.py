from django.db import models


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    enrollment_date = models.DateField()

    class_assignment = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="enrolled_students",
    )

    courses = models.ManyToManyField(
        Course,
        related_name="students",
        blank=True,
    )


class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(max_length=255)
    bio = models.TextField(null=True, blank=True)
