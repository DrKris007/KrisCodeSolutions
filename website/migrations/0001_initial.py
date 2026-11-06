import django.db.models.deletion
from django.db import migrations, models

import website.defaults as d


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("about_description", models.TextField(default=d.DEFAULT_ABOUT)),
                ("mission", models.TextField(default=d.DEFAULT_MISSION)),
                ("vision", models.TextField(default=d.DEFAULT_VISION)),
                ("cta_heading", models.CharField(default=d.DEFAULT_CTA_HEADING, max_length=200)),
                ("cta_text", models.TextField(default=d.DEFAULT_CTA_TEXT)),
                ("whatsapp_number", models.CharField(default=d.DEFAULT_WHATSAPP_NUMBER, max_length=30)),
                ("whatsapp_url", models.URLField(default=d.DEFAULT_WHATSAPP_URL, max_length=300)),
                ("email", models.EmailField(default=d.DEFAULT_EMAIL, max_length=254)),
                ("tiktok_url", models.URLField(blank=True, default=d.DEFAULT_TIKTOK, max_length=300)),
                ("instagram_url", models.URLField(blank=True, default=d.DEFAULT_INSTAGRAM, max_length=300)),
                ("x_url", models.URLField(blank=True, default=d.DEFAULT_X, max_length=300)),
                ("linkedin_url", models.URLField(blank=True, default=d.DEFAULT_LINKEDIN, max_length=300)),
            ],
            options={"verbose_name": "site settings", "verbose_name_plural": "site settings"},
        ),
        migrations.CreateModel(
            name="ProjectCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"verbose_name_plural": "project categories", "ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField(blank=True, max_length=170, unique=True)),
                ("project_type", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(blank=True, upload_to="projects/")),
                ("image_alt", models.CharField(blank=True, max_length=200)),
                ("is_featured", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project_url", models.URLField(blank=True, max_length=300)),
                ("show_external_link", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="projects",
                        to="website.projectcategory",
                    ),
                ),
            ],
            options={"ordering": ["order", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("icon_class", models.CharField(default="bi-code-slash", max_length=60)),
                ("image", models.ImageField(blank=True, upload_to="services/")),
                ("cta_label", models.CharField(default="Discuss This Service", max_length=60)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("role", models.CharField(max_length=120)),
                ("image", models.ImageField(blank=True, upload_to="team/")),
                ("bio", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="ContactInquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "New"),
                            ("contacted", "Contacted"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                        ],
                        default="new",
                        max_length=20,
                    ),
                ),
                ("notification_sent", models.BooleanField(default=False)),
                ("admin_notes", models.TextField(blank=True)),
            ],
            options={"verbose_name_plural": "contact inquiries", "ordering": ["-created_at"]},
        ),
    ]
