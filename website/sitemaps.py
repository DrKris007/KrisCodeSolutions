from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["website:home", "website:about", "website:services", "website:projects", "website:contact"]

    def location(self, item):
        return reverse(item)
