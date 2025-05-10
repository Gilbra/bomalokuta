# accounts/admin.py

from django.contrib import admin
from django.utils.html import format_html

from accounts.models import *

class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1  # Nombre de notifications à afficher par défaut
    fields = ('message', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

class SupportTicketInline(admin.TabularInline):
    model = SupportTicket
    extra = 1  # Nombre de tickets à afficher par défaut
    fields = ('subject', 'is_resolved', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_avatar', 'username', 'email', 'email_verified', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'email_verified')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('email_validation_token',)
    
    inlines = [NotificationInline, SupportTicketInline]

    actions = ['mark_as_verified', 'mark_as_unverified']

    def mark_as_verified(self, request, queryset):
        queryset.update(email_verified=True)
        self.message_user(request, "Les utilisateurs sélectionnés ont été marqués comme vérifiés.")
    mark_as_verified.short_description = "Marquer comme vérifiés"

    def mark_as_unverified(self, request, queryset):
        queryset.update(email_verified=False)
        self.message_user(request, "Les utilisateurs sélectionnés ont été marqués comme non vérifiés.")
    mark_as_unverified.short_description = "Marquer comme non vérifiés"

    def get_avatar(self, obj):
        """Affiche l'avatar sous forme de carré dans l'admin"""
        if obj.avatar:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.avatar.url)
        return "Pas d'image"
    
    get_avatar.short_description = 'Avatar'  # Titre de la colonne

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Les notifications sélectionnées ont été marquées comme lues.")
    mark_as_read.short_description = "Marquer comme lues"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Les notifications sélectionnées ont été marquées comme non lues.")
    mark_as_unread.short_description = "Marquer comme non lues"

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('subject', 'message')
    ordering = ('-created_at',)
    actions = ['mark_as_resolved', 'mark_as_unresolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, "Les tickets sélectionnés ont été marqués comme résolus.")
    mark_as_resolved.short_description = "Marquer comme résolus"

    def mark_as_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
        self.message_user(request, "Les tickets sélectionnés ont été marqués comme non résolus.")
    mark_as_unresolved.short_description = "Marquer comme non résolus"