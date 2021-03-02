from django.contrib import admin

from variables.models import Variable


class VariableAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "value_type", "definition_period"]
    filter_horizontal = ("dependencies",)
    list_filter = ("entity",)
    search_fields = ("name",)


admin.site.register(Variable, VariableAdmin)
