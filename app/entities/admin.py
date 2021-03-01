from django.contrib import admin

from entities.models import Entity

class EntityAdmin(admin.ModelAdmin):
    list_display = ["key", "label", "is_person"]

admin.site.register(Entity, EntityAdmin)
