from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Redirect logged-in users to a dashboard or profile page
        return redirect('jobs:home')  # replace 'dashboard' with your URL name
    return render(request, template_name='home/home.html')
