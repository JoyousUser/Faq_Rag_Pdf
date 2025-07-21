from django.contrib import admin
from .models import VisitLog

# Register your models here.

# à récupérer depuis la view avec : request.get_full_path()

@admin.register(VisitLog)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'url', 'timestamp')
    search_fields = ('user__username', 'url')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    fieldsets = (
    ("Historique", {
        'fields': ('user', 'url', 'timestamp')
    }),
    )
    readonly_fields = ('timestamp',)