from django.shortcuts import render



# About view
def about(request):
    return render(request, 'about/about.html')
