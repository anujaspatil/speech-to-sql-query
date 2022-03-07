from django.contrib import admin

# Register your models here.
from sql.models import Sql


@admin.register(Sql)
class SqlAdmin(admin.ModelAdmin):
    list_display = ('query1', 'created', 'user', 'output')
    search_fields = ['query1']
