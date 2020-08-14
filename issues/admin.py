from django.contrib import admin
from . import models


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'topic', 'priority', 'status']
    list_editable = ['author', 'topic', 'priority', 'status']


admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Comment)
