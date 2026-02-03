from django.http import HttpResponse
from django.shortcuts import render

from .models import Sample

# from .pagination import CustomPagination
# from .serializers import SampleSerializer


def sample_list(request):
    samples = Sample.objects.all()
    return render(request, "appendixapp/list.html", {"samples": samples})


def sample_detail(request, id):
    sample = Sample.objects.get(id=id)
    return render(request, "appendixapp/detail.html", {"sample": sample})


def sample_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Sample.objects.create(name=name)
        return HttpResponse("Sample created successfully")

    return render(request, "appendixapp/create.html")


# def samples_paginator(request):
#     samples = Sample.objects.all()
#     paginator = Paginator(samples, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     return render(request, "appendixapp/sample_list.html", {"page_obj": page_obj})


# class SampleViewSet(viewsets.ModelViewSet):
#     serializer_class = SampleSerializer
#     pagination_class = CustomPagination
