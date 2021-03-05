from django.contrib import admin

from variables.models import Variable


# class FormulaVariableInline(admin.TabularInline):
#     model = FormulaVariable
#     fk_name = "parent"


class VariableAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "value_type", "definition_period"]
    # inlines = (FormulaVariableInline,)  # ?
    list_filter = ("entity",)
    search_fields = ("name",)


admin.site.register(Variable, VariableAdmin)
# cannot register FormulaVariable?
