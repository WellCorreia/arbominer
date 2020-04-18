from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import TextMining
from django.http import JsonResponse

def index(request):
    return render(request, 'textmining.html')

def extractInformation(request):
    tags = request.POST.getlist('tags[]')
    virus = request.POST.get('virus')
    analise = request.POST.get('analise')
    result = None
    textmining = TextMining
    result = textmining.getWords(None, tags, virus, analise)
    return JsonResponse(result)