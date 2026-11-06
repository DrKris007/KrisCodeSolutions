from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactInquiry, Project, SiteSettings

VALID = {
    "full_name": "Ada Obi",
    "email": "ada@example.com",
    "subject": "New website",
    "message": "I would like a modern website for my small business, please.",
    "website": "",
}


class PageTests(TestCase):
    def test_all_pages_load(self):
        for name in ["home", "about", "services", "projects", "contact"]:
            response = self.client.get(reverse(f"website:{name}"))
            self.assertEqual(response.status_code, 200, name)

    def test_empty_states_render(self):
        self.assertContains(self.client.get(reverse("website:projects")), "No projects")

    def test_site_settings_defaults(self):
        self.assertIn("KrisCodeSolutions", SiteSettings.load().about_description)

    def test_projects_never_expose_unapproved_links(self):
        Project.objects.create(
            name="Acadestine", description="Education platform.", project_url="https://example.org/secret"
        )
        response = self.client.get(reverse("website:projects"))
        self.assertNotContains(response, "https://example.org/secret")

    def test_approved_link_is_shown_only_when_enabled(self):
        Project.objects.create(
            name="Approved", description="x", project_url="https://example.org/ok", show_external_link=True
        )
        self.assertContains(self.client.get(reverse("website:projects")), "https://example.org/ok")


class ContactTests(TestCase):
    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse("website:contact"), VALID)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactInquiry.objects.count(), 1)
        self.assertEqual(ContactInquiry.objects.get().status, "new")

    def test_invalid_submission_is_rejected(self):
        data = dict(VALID, message="short")
        response = self.client.post(reverse("website:contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        self.client.post(reverse("website:contact"), dict(VALID, website="http://spam"))
        self.assertEqual(ContactInquiry.objects.count(), 0)

    @override_settings(
        CONTACT_NOTIFY_EMAIL="owner@example.com",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_notification_flag_only_set_when_email_sent(self):
        self.client.post(reverse("website:contact"), VALID)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(ContactInquiry.objects.get().notification_sent)

    @override_settings(CONTACT_NOTIFY_EMAIL="")
    def test_no_notification_when_not_configured(self):
        self.client.post(reverse("website:contact"), VALID)
        self.assertFalse(ContactInquiry.objects.get().notification_sent)
