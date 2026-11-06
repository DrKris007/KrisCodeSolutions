from django.db import models
from django.utils.text import slugify

from . import defaults as d


class SiteSettings(models.Model):
    """Single-row table holding editable website content."""

    about_description = models.TextField(default=d.DEFAULT_ABOUT)
    mission = models.TextField(default=d.DEFAULT_MISSION)
    vision = models.TextField(default=d.DEFAULT_VISION)
    cta_heading = models.CharField(max_length=200, default=d.DEFAULT_CTA_HEADING)
    cta_text = models.TextField(default=d.DEFAULT_CTA_TEXT)
    whatsapp_number = models.CharField(max_length=30, default=d.DEFAULT_WHATSAPP_NUMBER)
    whatsapp_url = models.URLField(max_length=300, default=d.DEFAULT_WHATSAPP_URL)
    email = models.EmailField(default=d.DEFAULT_EMAIL)
    tiktok_url = models.URLField(max_length=300, blank=True, default=d.DEFAULT_TIKTOK)
    instagram_url = models.URLField(max_length=300, blank=True, default=d.DEFAULT_INSTAGRAM)
    x_url = models.URLField(max_length=300, blank=True, default=d.DEFAULT_X)
    linkedin_url = models.URLField(max_length=300, blank=True, default=d.DEFAULT_LINKEDIN)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the saved settings, or an unsaved instance holding the defaults."""
        return cls.objects.filter(pk=1).first() or cls()


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "project categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
    )
    project_type = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    project_url = models.URLField(max_length=300, blank=True)
    show_external_link = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "project"
            slug, n = base, 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def public_url(self):
        """An external link is only ever shown when explicitly approved in admin."""
        return self.project_url if (self.show_external_link and self.project_url) else ""


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=60, default="bi-code-slash")
    image = models.ImageField(upload_to="services/", blank=True)
    cta_label = models.CharField(max_length=60, default="Discuss This Service")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    image = models.ImageField(upload_to="team/", blank=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class ContactInquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    notification_sent = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "contact inquiries"

    def __str__(self):
        return f"{self.full_name}: {self.subject}"
