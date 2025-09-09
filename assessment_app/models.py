from django.db import models
from django.contrib.auth.models import User
import json

class SportAssessment(models.Model):
    SPORT_CHOICES = [
        ('Javelin Throw', 'Javelin Throw'),
        ('Table Tennis', 'Table Tennis'),
        ('Archery', 'Archery'),
        ('Push-ups', 'Push-ups'),
        ('Discus Throw', 'Discus Throw'),
        ('High Jump', 'High Jump'),
        ('Other Sports', 'Other Sports'),  # Add this line
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField(upload_to='assessment_videos/')
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    predicted_sport = models.CharField(max_length=50, blank=True)
    metrics = models.TextField(blank=True)
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def get_metrics(self):
        if self.metrics:
            try:
                return json.loads(self.metrics)
            except:
                return {}
        return {}
    
    def __str__(self):
        return f"{self.sport_type} Assessment - {self.created_at.strftime('%Y-%m-%d %H:%M')}"