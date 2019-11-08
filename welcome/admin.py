from django.contrib import admin

from .models import PageView, Choice, Question

# Register your models here.

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'timestamp']

admin.site.register(PageView, PageViewAdmin)
admin.site.register(Question)
admin.site.register(Choice)
