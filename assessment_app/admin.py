from django.contrib import admin
from .models import SportAssessment

@admin.register(SportAssessment)
class SportAssessmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'sport_type', 'predicted_sport', 'rating', 'created_at', 'processed']
    list_filter = ['sport_type', 'processed', 'created_at']
    search_fields = ['user__username', 'sport_type']
    readonly_fields = ['created_at', 'processed', 'predicted_sport', 'rating']
    
    def has_add_permission(self, request):
        return False