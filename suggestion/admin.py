from django.contrib import admin
from .models import Category,Organization,ComplaintSuggestion,ComplaintImage

# Register your models here.

admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(ComplaintImage)
admin.site.register(ComplaintSuggestion)