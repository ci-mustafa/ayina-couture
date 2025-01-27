from django.shortcuts import render



# Contact view
def contact(request):
    return render(request, 'contact/contact.html')
