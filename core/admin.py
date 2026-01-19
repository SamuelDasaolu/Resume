from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import (
    Profile, SocialLink, SkillCategory, Skill, Project, ProjectCategory,
    Experience, Education, Certification, Award, Service, Stat, ContactMessage
)

# Unregister default admin classes if they are already registered
# This prevents errors if this file is reloaded
try:
    admin.site.unregister(Project)
    admin.site.unregister(Service)
    admin.site.unregister(SkillCategory)
except admin.sites.NotRegistered:
    pass

# --- Inlines ---

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('name', 'level')
    ordering = ('order',)

# --- ModelAdmins ---

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'location', 'updated_at')
    search_fields = ('full_name', 'title')
    fieldsets = (
        (None, {
            'fields': ('full_name', 'title', 'summary')
        }),
        ('Contact & Location', {
            'fields': ('email', 'location')
        }),
        ('Files', {
            'fields': ('headshot', 'resume_file'),
            'description': "Note: For dummy data, these are URLs. In production, they are file uploads."
        }),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(OrderedModelAdmin):
    list_display = ('label', 'url', 'move_up_down_links')
    list_editable = ('url',)
    ordering = ('order',)
    fields = ('label', 'url', 'icon_class')
    search_fields = ('label',)
    help_texts = {
        'icon_class': "Example: 'bi bi-github' for a GitHub icon. Uses Bootstrap Icons."
    }

@admin.register(SkillCategory)
class SkillCategoryAdmin(OrderedModelAdmin):
    list_display = ('name', 'move_up_down_links')
    inlines = [SkillInline]
    ordering = ('order',)

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(OrderedModelAdmin):
    list_display = ('title', 'category', 'featured', 'move_up_down_links')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'description', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'description')
        }),
        ('Technical Details', {
            'fields': ('tech_stack', 'repo_url', 'live_url')
        }),
        ('Media & Ordering', {
            'fields': ('image', 'featured'),
            'description': "Note: For dummy data, 'image' is a URL. In production, it's a file upload."
        }),
    )

@admin.register(Experience)
class ExperienceAdmin(OrderedModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'move_up_down_links')
    search_fields = ('role', 'company')
    ordering = ('order',)

@admin.register(Education)
class EducationAdmin(OrderedModelAdmin):
    list_display = ('school', 'program', 'start_date', 'end_date', 'move_up_down_links')
    search_fields = ('school', 'program')
    ordering = ('order',)

@admin.register(Certification)
class CertificationAdmin(OrderedModelAdmin):
    list_display = ('name', 'issuer', 'issue_date', 'move_up_down_links')
    search_fields = ('name', 'issuer')
    ordering = ('order',)

@admin.register(Service)
class ServiceAdmin(OrderedModelAdmin):
    list_display = ('title', 'featured', 'move_up_down_links')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Visuals & Ordering', {
            'fields': ('icon_class', 'image', 'featured'),
            'description': "Note: For dummy data, 'image' is a URL. In production, it's a file upload."
        }),
    )

@admin.register(Stat)
class StatAdmin(OrderedModelAdmin):
    list_display = ('label', 'count', 'icon_class', 'move_up_down_links')
    list_editable = ('count', 'icon_class')
    ordering = ('order',)

@admin.register(Award)
class AwardAdmin(OrderedModelAdmin):
    list_display = ('title', 'issuer', 'year', 'move_up_down_links')
    search_fields = ('title', 'issuer')
    ordering = ('order',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'read', 'created_at')
    list_filter = ('read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

# Note: The Skill model is managed via the SkillCategoryAdmin inline.
# If you need to register it directly, you can do so like this:
# @admin.register(Skill)
# class SkillAdmin(OrderedModelAdmin):
#     list_display = ('name', 'category', 'level', 'move_up_down_links')
#     list_filter = ('category',)
#     search_fields = ('name',)
#     ordering = ('order',)
