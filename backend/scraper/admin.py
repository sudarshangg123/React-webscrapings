from django.contrib import admin
from .models import ScrapedItem

@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'scraped_at')
    search_fields = ('title', 'source')
