from django.contrib import admin
from .models import File


# I register my File model in my admin so I am able to inspect in my django admin interface
class FileAdmin(admin.ModelAdmin):
    list_display = ["chrom", "pos", "id", "ref", "alt"]


admin.site.register(File, FileAdmin)
