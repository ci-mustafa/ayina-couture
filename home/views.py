from django.shortcuts import render, redirect
from .forms import NewsletterForm
from django.contrib import messages


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


# newsletter view
def newsletter_subscribe(request):
    """
    Handle newsletter subscription form submissions.

    This view processes POST requests containing
    newsletter subscription data.
    - If the form is valid, the email is saved to the database,
    and a success message is displayed.
    - If the form is invalid (e.g., duplicate email or incorrect format),
    an error message is shown.
    - After processing, the user is redirected to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the home page.
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
            "You have successfully subscribed to our newsletter!")
        else:
            messages.error(request, "Invalid email or email already exists.")
    return redirect("home")