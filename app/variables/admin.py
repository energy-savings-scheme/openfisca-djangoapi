from django.contrib import admin

from variables.models import Variable

class VariableAdmin(admin.ModelAdmin):
    list_display = ["variable_name"]

admin.site.register(Variable, VariableAdmin)
