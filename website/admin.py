from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    ContactInquiry,
    Project,
    ProjectCategory,
    Service,
    SiteSettings,
    TeamMember,
)

admin.site.site_header = "KrisCodeSolutions Administration"
admin.site.site_title = "KrisCodeSolutions Admin"
admin.site.index_title = "Manage your website"


def _thumb(obj, size=56):
    if obj.image:
        return format_html(
            '<img src="{}" alt="" style="width:{}px;height:{}px;object-fit:cover;object-position:top;border-radius:6px;">',
            obj.image.url, size, size,
        )
    return "-"


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "name", "category", "project_type", "is_featured", "is_active", "order", "created_at")
    list_display_links = ("thumbnail", "name")
    list_editable = ("is_featured", "is_active", "order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("name", "description", "project_type")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview", "created_at")
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "project_type", "description")}),
        ("Preview image", {
            "fields": ("image", "image_preview", "image_alt"),
            "description": "Upload or replace the project's homepage preview / mockup here.",
        }),
        ("Display", {"fields": ("is_featured", "is_active", "order", "created_at")}),
        ("Optional external link", {
            "fields": ("project_url", "show_external_link"),
            "description": (
                "Leave 'Show external link' unticked to keep the project a static preview. "
                "A link is only displayed publicly when you tick the box AND provide an approved URL."
            ),
        }),
    )

    @admin.display(description="Preview")
    def thumbnail(self, obj):
        return _thumb(obj)

    @admin.display(description="Current image")
    def image_preview(self, obj):
        return _thumb(obj, 240) if obj.pk else "Save the project to see the preview."


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    fieldsets = (
        (None, {"fields": ("title", "description", "cta_label")}),
        ("Icon / image", {
            "fields": ("icon_class", "image"),
            "description": "Icon class uses Bootstrap Icons names, e.g. bi-code-slash, bi-cart3, bi-phone. An uploaded image replaces the icon.",
        }),
        ("Display", {"fields": ("order", "is_active")}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "bio")


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "email", "subject", "status", "notification_sent")
    list_editable = ("status",)
    list_filter = ("status", "created_at", "notification_sent")
    search_fields = ("full_name", "email", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("full_name", "email", "subject", "message", "created_at", "notification_sent")
    fieldsets = (
        ("Inquiry", {"fields": ("full_name", "email", "subject", "message", "created_at", "notification_sent")}),
        ("Management", {"fields": ("status", "admin_notes")}),
    )
    actions = ["mark_contacted", "mark_in_progress", "mark_completed"]

    def has_add_permission(self, request):
        return False  # inquiries only arrive through the public form

    def _set_status(self, request, queryset, status, label):
        updated = queryset.update(status=status)
        self.message_user(request, f"{updated} inquiry(ies) marked as {label}.", messages.SUCCESS)

    @admin.action(description="Mark selected as Contacted")
    def mark_contacted(self, request, queryset):
        self._set_status(request, queryset, ContactInquiry.Status.CONTACTED, "Contacted")

    @admin.action(description="Mark selected as In Progress")
    def mark_in_progress(self, request, queryset):
        self._set_status(request, queryset, ContactInquiry.Status.IN_PROGRESS, "In Progress")

    @admin.action(description="Mark selected as Completed")
    def mark_completed(self, request, queryset):
        self._set_status(request, queryset, ContactInquiry.Status.COMPLETED, "Completed")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("About", {"fields": ("about_description", "mission", "vision")}),
        ("Call-to-action", {"fields": ("cta_heading", "cta_text")}),
        ("Contact information", {"fields": ("whatsapp_number", "whatsapp_url", "email")}),
        ("Social media", {"fields": ("tiktok_url", "instagram_url", "x_url", "linkedin_url")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.objects.first()
        if obj:
            return redirect(reverse("admin:website_sitesettings_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)
