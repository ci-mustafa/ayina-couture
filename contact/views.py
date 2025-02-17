from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm


def contact(request):
    """
    Handle the contact form submission and email notification.
    This view processes the contact form on both GET and POST requests.
    On POST, it validates the user's input, saves the contact data to
    the database, and sends an email notification to the site admin.
    If the email is sent successfully, a success message is displayed;
    otherwise, an error message is shown.
    Args:
        request (HttpRequest): The incoming HTTP request from the user.
    Returns:
        HttpResponse: Renders the contact page on GET requests or after
        processing the form.
    Context:
        contact_form (ContactForm): The form instance,
        populated with data on POST requests
        or empty for GET requests.
    Template:
        contact.html: The template that displays the
        contact form and feedback messages.
    """
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            # Save the form data to the database
            contact_form.save()

            # Email configuration
            subject = 'New Contact Form Submission'
            message = (
                f"Name: {contact_form.cleaned_data['name']}\n"
                f"Email: {contact_form.cleaned_data['email']}\n"
                f"Message:\n{contact_form.cleaned_data['message']}"
            )
            from_email = settings.EMAIL_HOST_USER  # Site's email address
            recipient_list = ['ayina.couture@gmail.com']  # Admin's email add
            # Construct the email message
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
                headers={'Reply-To': contact_form.cleaned_data['email']}
            )

            try:
                # Attempt to send the email
                email.send(fail_silently=False)
                # Success message
                messages.success(request,
                                 f"Dear {contact_form.cleaned_data['name']},\
                                 your message has been sent successfully!")
                return redirect('contact')  # Redirect back to the contact page
            except Exception as e:
                # Email sending failed
                messages.error(request, f"An error occurred while\
                sending the email: {str(e)}")
                return redirect('contact')
    else:
        # For GET requests, render an empty form
        contact_form = ContactForm()

    # Render the contact page with the form
    return render(request, 'contact/contact.html', {
        'contact_form': contact_form
    })


