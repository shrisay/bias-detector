from django.db import models

# Create your models here.

class Feedback(models.Model):
    article_url = models.URLField()
    bias_label = models.CharField(max_length=50)   # e.g., "neutral", "sensationalism"
    agree = models.BooleanField(default=True)      # True = agree, False = disagree
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.article_url} ({self.bias_label})"