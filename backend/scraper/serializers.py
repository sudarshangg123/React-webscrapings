from rest_framework import serializers
from .models import ScrapedItem

class ScrapedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedItem
        fields = ['id', 'title', 'url', 'summary', 'source', 'scraped_at']
