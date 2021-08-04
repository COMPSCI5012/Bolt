from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context_dict = {'boldmessage': 'YOLO'}
    return render(request, 'bolt/index.html', context=context_dict)

def about(request):
    return render(request, 'bolt/about.html')