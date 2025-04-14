from django.shortcuts import render
from django.views import View
from suggestion.models import Category

# Create your views here.

class HomeView(View):
    def get(self,request):
        categories = Category.objects.all()
        context = {
            'categories':categories
        }
        return render(request, 'main/home.html',context)
