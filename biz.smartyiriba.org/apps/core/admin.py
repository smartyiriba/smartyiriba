from django.contrib import admin
from .models import ContactMessage, ShowcaseEntry, TrainingSession
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'processed')
    list_filter = ('processed',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'phone', 'organization', 'subject', 'message', 'created_at')
    def has_add_permission(self, request): return False
@admin.register(ShowcaseEntry)
class ShowcaseEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'published', 'position')
    list_filter = ('kind', 'published')
@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'price', 'program', 'published')
    list_filter = ('published', 'program')
