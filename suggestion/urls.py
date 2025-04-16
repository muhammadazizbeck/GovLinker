from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/',views.CategoryDetailView.as_view(),name='category_detail')
]