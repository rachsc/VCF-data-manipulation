from django.contrib import admin
from .models import VcfRow


# I register my model in my admin so I am able to inspect in my django admin interface
class VcfRowAdmin(admin.ModelAdmin):
    list_display = ["CHROM", "POS", "ID", "REF", "ALT"]


admin.site.register(VcfRow, VcfRowAdmin)
