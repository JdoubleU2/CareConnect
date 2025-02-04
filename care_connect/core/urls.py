from django.urls import path
from . import views

urlpatterns = [
    path('', views.core_view, name='core'),  # Maps the root URL to the chat_view
]