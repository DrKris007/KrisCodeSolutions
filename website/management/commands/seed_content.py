"""Create the initial site content: settings, categories, services and the four portfolio projects.

Safe to run more than once. It never overwrites text you have edited in the admin and only
attaches a preview image when a project has none yet.
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from website.models import Project, ProjectCategory, Service, SiteSettings

IMAGES_DIR = Path(__file__).resolve().parents[2] / "static" / "website" / "images"

CATEGORIES = [
    "E-commerce / Online Store",
    "Education / Programming Platform",
    "Charity / Non-profit",
    "Banking / Financial Services",
]

PROJECTS = [
    {
        "name": "Matty Store",
        "category": "E-commerce / Online Store",
        "project_type": "E-commerce website (concept preview)",
        "description": (
            "An e-commerce online store designed to provide customers with a convenient shopping "
            "experience, allowing them to explore products and make purchases through a modern "
            "digital storefront."
        ),
        "image_file": "matty-store-mockup.png",
        "image_alt": "Conceptual mockup of the Matty Store e-commerce homepage",
    },
    {
        "name": "Acadestine",
        "category": "Education / Programming Platform",
        "project_type": "Education platform",
        "description": (
            "A technology education platform designed to help learners develop practical technical "
            "skills through interactive lessons, expert-led courses and real-world projects."
        ),
        "image_file": "acadestine-homepage.png",
        "image_alt": "Screenshot of the Acadestine homepage",
    },
    {
        "name": "BigDaddy Charity Foundation",
        "category": "Charity / Non-profit",
        "project_type": "Non-profit website (concept preview)",
        "description": (
            "A charity organisation website concept focused on presenting the foundation's mission, "
            "highlighting its initiatives, raising awareness and helping supporters connect with "
            "meaningful causes."
        ),
        "image_file": "bigdaddy-charity-mockup.png",
        "image_alt": "Conceptual mockup of the BigDaddy Charity Foundation homepage",
    },
    {
        "name": "Capital City Trust",
        "category": "Banking / Financial Services",
        "project_type": "Financial services website",
        "description": (
            "A financial services website project designed to present banking information, financial "
            "products and services through a structured, modern and user-friendly digital experience."
        ),
        "image_file": "capital-city-trust-homepage.png",
        "image_alt": "Screenshot of the Capital City Trust homepage",
    },
]

SERVICES = [
    ("Website Design & Development", "bi-window-desktop",
     "Creating modern, responsive and user-friendly websites that represent businesses professionally.",
     "Get a Website"),
    ("Web Application Development", "bi-code-slash",
     "Developing functional web applications that solve business problems and improve operations.",
     "Discuss Your App"),
    ("E-commerce Development", "bi-cart3",
     "Building online stores that allow businesses to showcase products, manage purchases and reach customers.",
     "Build Your Store"),
    ("Website Management & Maintenance", "bi-gear",
     "Providing website updates, maintenance, technical support and ongoing improvements.",
     "Get Support"),
    ("Responsive Website Optimization", "bi-phone",
     "Ensuring websites work smoothly across desktop computers, tablets and mobile devices.",
     "Optimise My Site"),
]


class Command(BaseCommand):
    help = "Create the initial KrisCodeSolutions content (settings, categories, services, projects)."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(pk=1)
        self.stdout.write("Site settings ready.")

        categories = {}
        for i, name in enumerate(CATEGORIES, start=1):
            categories[name], _ = ProjectCategory.objects.get_or_create(name=name, defaults={"order": i})

        for i, (title, icon, description, cta) in enumerate(SERVICES, start=1):
            Service.objects.get_or_create(
                title=title,
                defaults={"icon_class": icon, "description": description, "cta_label": cta, "order": i},
            )
        self.stdout.write(f"Services ready ({Service.objects.count()}).")

        for i, data in enumerate(PROJECTS, start=1):
            project, created = Project.objects.get_or_create(
                name=data["name"],
                defaults={
                    "category": categories[data["category"]],
                    "project_type": data["project_type"],
                    "description": data["description"],
                    "image_alt": data["image_alt"],
                    "order": i,
                    "is_featured": True,
                    "is_active": True,
                    "show_external_link": False,
                },
            )
            if not project.image:
                source = IMAGES_DIR / data["image_file"]
                if source.exists():
                    with source.open("rb") as handle:
                        project.image.save(data["image_file"], File(handle), save=True)
                    self.stdout.write(self.style.SUCCESS(f"  {project.name}: image attached."))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"  {project.name}: image NOT found. Save it as "
                        f"website/static/website/images/{data['image_file']} and run this command again "
                        f"(or upload it in the admin)."
                    ))
            else:
                self.stdout.write(f"  {project.name}: already has an image.")

        self.stdout.write(self.style.SUCCESS("Initial content is ready."))
