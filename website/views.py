import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm
from .models import Project, Service, TeamMember

logger = logging.getLogger(__name__)


def _active_services():
    return Service.objects.filter(is_active=True)


def _active_projects():
    return Project.objects.filter(is_active=True).select_related("category")


def _active_team():
    return TeamMember.objects.filter(is_active=True)


def home(request):
    return render(request, "website/home.html", {
        "meta_title": "KrisCodeSolutions | We Build Websites and Apps",
        "meta_description": (
            "KrisCodeSolutions designs and develops modern websites, web applications and "
            "digital solutions that help businesses grow online."
        ),
        "services": _active_services(),
        "projects": _active_projects().filter(is_featured=True)[:6],
        "team_members": _active_team(),
    })


def about(request):
    return render(request, "website/about.html", {
        "meta_title": "About Us | KrisCodeSolutions",
        "meta_description": (
            "Learn about KrisCodeSolutions, our mission and our vision to be a trusted "
            "digital solutions partner for growing businesses."
        ),
        "team_members": _active_team(),
    })


def services(request):
    return render(request, "website/services.html", {
        "meta_title": "Services | KrisCodeSolutions",
        "meta_description": (
            "Website design and development, web applications, e-commerce, website "
            "maintenance and responsive optimisation from KrisCodeSolutions."
        ),
        "services": _active_services(),
    })


def projects(request):
    return render(request, "website/projects.html", {
        "meta_title": "Projects & Portfolio | KrisCodeSolutions",
        "meta_description": (
            "Explore selected digital projects by KrisCodeSolutions: e-commerce, education, "
            "charity and financial services websites."
        ),
        "projects": _active_projects(),
    })


def _send_notification(inquiry):
    """Email the site owner. Returns True only if an email was actually sent."""
    recipient = settings.CONTACT_NOTIFY_EMAIL
    if not recipient:
        return False
    body = (
        f"New website inquiry\n\n"
        f"Name: {inquiry.full_name}\n"
        f"Email: {inquiry.email}\n"
        f"Subject: {inquiry.subject}\n"
        f"Received: {inquiry.created_at:%Y-%m-%d %H:%M}\n\n"
        f"Message:\n{inquiry.message}\n"
    )
    try:
        email = EmailMessage(
            subject=f"[KrisCodeSolutions] {inquiry.subject}"[:150],
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[inquiry.email],
        )
        sent = email.send(fail_silently=False)
    except Exception:  # noqa: BLE001 - never lose an inquiry because email failed
        logger.exception("Could not send inquiry notification email")
        return False
    return bool(sent)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            if _send_notification(inquiry):
                inquiry.notification_sent = True
                inquiry.save(update_fields=["notification_sent"])
            messages.success(request, "Thank you! Your message has been received and we will get back to you soon.")
            return redirect(f"{reverse('website:contact')}#contact-form")
        messages.error(request, "Please correct the highlighted fields and try again.")
    else:
        initial = {}
        service = request.GET.get("service", "").strip()
        if service:
            initial["subject"] = f"Enquiry: {service}"[:200]
        form = ContactForm(initial=initial)

    return render(request, "website/contact.html", {
        "meta_title": "Contact Us | KrisCodeSolutions",
        "meta_description": "Start a project with KrisCodeSolutions. Message us on WhatsApp, send an email or use our contact form.",
        "form": form,
    })


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
