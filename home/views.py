from django.shortcuts import render


# Home page view
def index(request):
    """
    View function for rendering the home page of the site.
    This view is responsible for rendering the 'home/index.html' template
    which represents the main landing page of the website.
    Args:
        request (HttpRequest): The request object that contains metadata
        about the request.
    Returns:
        HttpResponse: The rendered HTML page for the home page.
    """
    return render(request, 'home/index.html')