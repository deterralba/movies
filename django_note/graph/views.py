from django.shortcuts import render
from django.http import HttpResponse

def get_graph(request, id):
    return HttpResponse('{}'.format(id))
