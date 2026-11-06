from django.db.utils import OperationalError, ProgrammingError

from .models import SiteSettings


def site(request):
    """Make editable site settings available in every template as `site`."""
    try:
        settings_obj = SiteSettings.load()
    except (OperationalError, ProgrammingError):
        # Database not migrated yet: fall back to built-in defaults.
        settings_obj = SiteSettings()
    return {"site": settings_obj}
