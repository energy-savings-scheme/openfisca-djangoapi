from django.contrib import admin

from entities.models import Entity

class EntityAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Entity, EntityAdmin)
