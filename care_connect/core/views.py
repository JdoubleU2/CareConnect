from django.shortcuts import render

# Create your views here.

def core_view(request):
    return render(request, 'core/core.html')  # Render the chat template