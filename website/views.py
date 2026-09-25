from django.shortcuts import render

def index(request):
    """
    Renders the public-facing landing page / portfolio for the school.
    """
    return render(request, 'website/index.html')
