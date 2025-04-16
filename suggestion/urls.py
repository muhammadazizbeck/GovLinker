from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:category_id>/',views.CategoryDetailView.as_view(),name='category_detail'),
    path('support/<int:suggestion_id>/', views.support_suggestion, name='support_suggestion'),

]