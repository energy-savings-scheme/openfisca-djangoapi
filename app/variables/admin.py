from django.contrib import admin

from variables.models import Variable


class VariableAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "value_type", "definition_period"]


admin.site.register(Variable, VariableAdmin)
