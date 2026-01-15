from django.shortcuts import render
from .models import Student

def get_all_student(request):
    #studentテーブルの全てのデータを取得
    students = Student.objects.all()
    #'educationapp/student_list.html'というテンプレートを使用して、studentsをcontextとして渡す
    return render(request, 'educationapp/student_list.html', {'students': students})
