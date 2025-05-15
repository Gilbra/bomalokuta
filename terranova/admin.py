from django.contrib import admin
from .models import CustomUser, Dechet, PointCollecte, Evenement, Statistique, Recompense

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_associated', 'points', 'role')
    search_fields = ('user_associated__username', 'role')
    list_filter = ('role',)
    ordering = ('user_associated',)

class DechetAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'statut', 'date_signalement')
    search_fields = ('description',)
    list_filter = ('statut', 'utilisateur')
    ordering = ('-date_signalement',)
    readonly_fields = ('date_signalement',)

class PointCollecteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'niveau_remplissage')
    search_fields = ('nom',)
    list_filter = ('type',)
    ordering = ('nom',)

class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'utilisateur', 'date', 'lieu')
    search_fields = ('titre', 'description')
    list_filter = ('date',)
    ordering = ('-date',)

class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'dechets_signalés', 'dechets_recyclés', 'date')
    search_fields = ('utilisateur__user_associated__username',)
    ordering = ('-date',)

class RecompenseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'points')
    search_fields = ('nom',)
    ordering = ('points',)

# Registering the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Dechet, DechetAdmin)
admin.site.register(PointCollecte, PointCollecteAdmin)
admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Statistique, StatistiqueAdmin)
admin.site.register(Recompense, RecompenseAdmin)