from django.shortcuts import render

def index(request):
    return render(request, 'inventory/index.html', {'module_name': 'inventory'})