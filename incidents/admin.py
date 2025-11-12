from django.contrib import admin
from .models import Incident
from constans import incidents

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("incident_short", "status_display", "source_display", "created_at")
    list_filter = ("status", "source", "created_at")
    search_fields = ("incident",)
    readonly_fields = ("created_at",)

    def incident_short(self, obj):
        # Показываем первые 30 символов текста для удобства
        return obj.incident[:30] + ("..." if len(obj.incident) > 30 else "")
    incident_short.short_description = "Incident"

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"

    def source_display(self, obj):
        return obj.get_source_display()
    source_display.short_description = "Source"
