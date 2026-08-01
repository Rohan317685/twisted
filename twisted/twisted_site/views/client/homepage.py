from django.views import View
from django.shortcuts import render
import os

# Create your views here.
class HomepageView(View):
    def get(self, request):
        if os.environ.get("LOGIN_ENABLED") == 'false':
            login_enabled = False
        else:
            login_enabled = True
        return render(request, "client/homepage.html", {"login_enabled": login_enabled})

class FaqsView(View):
    def get(self, request):
        return render(request, "client/faqs.html")