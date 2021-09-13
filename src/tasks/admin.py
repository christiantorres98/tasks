from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'status', 'created_date', 'delivery_date')
    list_display_links = list_display
    list_filter = ('user', 'status')
    search_fields = ('name', 'description')
    raw_id_fields = ('user',)
    readonly_fields = ('created_date',)
