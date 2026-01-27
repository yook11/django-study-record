from django.shortcuts import get_object_or_404, render

from .models import SchoolClass, Student


def get_all_student(request):
    # studentテーブルの全てのデータを取得
    students = Student.objects.all()
    #'educationapp/student_list.html'というテンプレートを使用して、studentsをcontextとして渡す
    return render(request, "educationapp/student_list.html", {"students": students})


def get_student_by_id(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "educationapp/student_detail.html", {"student": student})


def filter_students(request):
    students = Student.objects.all()
    name_query = request.GET.get("name")

    if name_query:
        students = students.filter(name__icontains=name_query)

    age_query = request.GET.get("age")
    age_operator = request.GET.get("age_operator")

    if age_query and age_operator:
        try:
            age_value = int(age_query)
            if age_operator == "lt":
                students = students.filter(age__lt=age_value)
            elif age_operator == "gt":
                students = students.filter(age__gt=age_value)
            elif age_operator == "eq":
                students = students.filter(age=age_value)
        except ValueError:
            pass

    return render(request, "educationapp/student_list.html", {"students": students})


def student_with_profile_list(request):
    students_with_profiles = Student.objects.select_related("profile")

    return render(
        request,
        "educationapp/student_with_profile_list.html",
        {"students_with_profiles": students_with_profiles},
    )


def class_students(request):
    classes = SchoolClass.objects.all()

    selected_class_id = request.GET.get("class_id")

    if selected_class_id:
        selected_class = SchoolClass.objects.get(id=selected_class_id)
        students = selected_class.enrolled_students.all()
    else:
        selected_class = None
        students = None

    return render(
        request,
        "educationapp/class_students.html",
        {
            "classes": classes,
            "selected_class": selected_class,
            "students": students,
        },
    )


def students_with_courses(request):
    students = Student.objects.prefetch_related("courses")

    return render(request, "educationapp/student_list_with_courses.html", {"students": students})
