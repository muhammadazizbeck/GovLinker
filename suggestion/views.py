from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Organization,ComplaintImage,ComplaintSuggestion
from django.views import View
from django.db.models import F
from django.contrib import messages
from suggestion.models import SuggestionSupport,SuggestionView

# Create your views here.

class CategoryDetailView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        suggestions = ComplaintSuggestion.objects.filter(category=category)
        context = {
            'suggestions': suggestions,
            'category': category
        }
        return render(request, 'suggestion/category_detail.html', context)
    
def support_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(ComplaintSuggestion, id=suggestion_id)

    if request.user.is_authenticated:
        obj, created = SuggestionSupport.objects.get_or_create(user=request.user, suggestion=suggestion)
        if created:
            suggestion.supports += 1
            suggestion.save()
            messages.success(request, "Taklifni qo‘llab-quvvatladingiz!")
        else:
            messages.warning(request, "Siz allaqachon qo‘llab-quvvatlagansiz.")
    else:
        messages.error(request, "Avval tizimga kiring.")

    return redirect('category_detail', category_id=suggestion.category.id)


def some_view(request, suggestion_id):
    suggestion = get_object_or_404(ComplaintSuggestion, id=suggestion_id)
    if request.user.is_authenticated:
        obj, created = SuggestionView.objects.get_or_create(user=request.user, suggestion=suggestion)
        if created:
            suggestion.views += 1
            suggestion.save()


    
#sfgfasfffffr
#ghgh
#ghdg

        


