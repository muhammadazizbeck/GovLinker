from django.shortcuts import render,get_object_or_404
from .models import Category,Organization,ComplaintImage,ComplaintSuggestion
from django.views import View

# Create your views here.

class SuggestionComplaintView(View):
    def get(self,request,category_id):
        category = get_object_or_404(Category,id=category_id)
        suggestions = ComplaintSuggestion.objects.filter(category=category)
        context = {
            'suggestions':suggestions
        }
        return render(request,'suggestion/suggestion.html' \
        '')


        


