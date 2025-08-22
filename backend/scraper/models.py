from django.db import models

class ScrapedItem(models.Model):
    title = models.TextField()
    url = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=200, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:80]
