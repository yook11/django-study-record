from django.shortcuts import render
from django.http import HttpResponse
from .models import Sample

def sample_list(request):
    samples = Sample.objects.all()
    return render(request, 'appendixapp/sample_list.html', {'samples': samples})

def sample_detail(request, id):
    sample = Sample.objects.get(id=id)
    return render(request, 'appendixapp/sample_detail.html', {'sample': sample})

def sample_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Sample.objects.create(name=name)
        return HttpResponse('Sample created successfully')
    
    return render(request, 'appendixapp/create.html')
