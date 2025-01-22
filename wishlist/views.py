from django.shortcuts import render




# wishlist view
def list_wishlist(request):
    return render(request, 'wishlist/wishlist.html')
