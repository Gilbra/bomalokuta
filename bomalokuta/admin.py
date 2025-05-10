# accounts/admin.py

from django.contrib import admin
from bomalokuta.models import *

class SubmissionElementInline(admin.TabularInline):
    model = SubmissionElement
    extra = 1
    #fields = ('content_type', 'content', 'order', 'created_at')
    #readonly_fields = ('created_at',)
    can_delete = True

class VerificationInline(admin.TabularInline):
    model = Verification
    extra = 1
    fields = ('expert', 'verification_date', 'is_verified', 'next_verification_date', 'comments')
    readonly_fields = ('verification_date',)
    can_delete = True

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_associated', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('user_associated__username', 'role')
    ordering = ('-created_at',)
    #inlines = [SubmissionElementInline]

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Les utilisateurs sélectionnés ont été activés.")
    activate_users.short_description = "Activer les utilisateurs"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Les utilisateurs sélectionnés ont été désactivés.")
    deactivate_users.short_description = "Désactiver les utilisateurs"

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'submission_date', 'updated_at', 'status', 'priority')
    list_filter = ('status', 'priority', 'submission_date')
    search_fields = ('label',)
    ordering = ('-submission_date',)
    inlines = [SubmissionElementInline, VerificationInline]

@admin.register(SubmissionElement)
class SubmissionElementAdmin(admin.ModelAdmin):
    list_display = ('submission', 'content_type', 'order', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('content',)
    ordering = ('submission', 'order', 'created_at')

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('submission', 'expert', 'verification_date', 'is_verified')
    list_filter = ('is_verified', 'verification_date')
    search_fields = ('comments',)
    ordering = ('-verification_date',)
    actions = ['mark_as_verified', 'mark_as_unverified']

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Les vérifications sélectionnées ont été marquées comme vérifiées.")
    mark_as_verified.short_description = "Marquer comme vérifiées"

    def mark_as_unverified(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, "Les vérifications sélectionnées ont été marquées comme non vérifiées.")
    mark_as_unverified.short_description = "Marquer comme non vérifiées"

@admin.register(TextAnalysis)
class TextAnalysisAdmin(admin.ModelAdmin):
    list_display = ('submission', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('submission__label',)
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('submission', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment',)
    ordering = ('-created_at',)

@admin.register(DisinformationTrend)
class DisinformationTrendAdmin(admin.ModelAdmin):
    list_display = ('trend_type', 'alert_level', 'created_at')
    list_filter = ('trend_type', 'alert_level', 'created_at')
    search_fields = ('trend_data',)
    ordering = ('-created_at',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status', 'is_archived')
    list_filter = ('status', 'is_archived', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    actions = ['archive_conversations', 'unarchive_conversations']

    def archive_conversations(self, request, queryset):
        queryset.update(is_archived=True)
        self.message_user(request, "Les conversations sélectionnées ont été archivées.")
    archive_conversations.short_description = "Archiver les conversations"

    def unarchive_conversations(self, request, queryset):
        queryset.update(is_archived=False)
        self.message_user(request, "Les conversations sélectionnées ont été désarchivées.")
    unarchive_conversations.short_description = "Désarchiver les conversations"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'user', 'created_at', 'message_type')
    list_filter = ('message_type', 'created_at')
    search_fields = ('content',)
    ordering = ('-created_at',)
