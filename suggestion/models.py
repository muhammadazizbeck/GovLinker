from django.db import models
from users.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name
    

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class ComplaintSuggestion(models.Model):
    CATEGORY_CHOICES = [
        ('complaint', 'Shikoyat'),
        ('suggestion', 'Taklif'),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name='complaints')
    status = models.CharField(max_length=20, choices=[
        ('new', 'Yangi'),
        ('in_progress', "Ko‘rib chiqilmoqda"),
        ('resolved', 'Hal qilindi'),
    ], default='new')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ComplaintImage(models.Model):
    complaint = models.ForeignKey(ComplaintSuggestion, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='complaint_images/', default='images/suggestion-image.png')

    def __str__(self):
        return f"Image for {self.complaint.title}"