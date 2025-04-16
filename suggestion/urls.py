from django.urls import path
from . import views

urlpatterns = [
    path('',views.SuggestionComplaintView.as_view(),name='suggestions')
]