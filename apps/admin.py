from django.contrib import admin

from apps.models import Stadium


# Register your models here.
@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    ...
