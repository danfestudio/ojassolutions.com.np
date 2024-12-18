from django.shortcuts import render
from .models import AboutUs, Testimonial, Service
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.core.cache import cache  # For rate limiting
from .forms import ContactSubmissionForm


def home(request):
    # Fetch the latest AboutUs entry (assuming there’s only one)
    about_us = AboutUs.objects.first()

    # Fetch all testimonials and services
    testimonials = Testimonial.objects.all()
    services = Service.objects.all()

    # Pass the fetched data to the template as context
    context = {
        'about_us': about_us,
        'testimonials': testimonials,
        'services': services,
    }

    return render(request, 'website/index.html', context)



def submit_contact(request):
    if request.method == 'POST':
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            # Rate limiting logic
            user_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            recent_submissions = cache.get(user_key, [])

            # Check if the user has exceeded the limit
            time_threshold = now() - timedelta(minutes=60)
            recent_submissions = [ts for ts in recent_submissions if ts > time_threshold]

            if len(recent_submissions) >= 2:
                return JsonResponse({"error": "We have already received your message. We will get back to you soon."}, status=429)

            # Save submission and update cache
            form.save()
            recent_submissions.append(now())
            cache.set(user_key, recent_submissions, timeout=600)  # Cache for 10 minutes

            return JsonResponse({"success": "Your message has been submitted successfully!"})
        else:
            return JsonResponse({"error": "Invalid form submission. Please check your inputs."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)