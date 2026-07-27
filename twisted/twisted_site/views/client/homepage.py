from django.views import View
from django.shortcuts import render

# Create your views here.
class HomepageView(View):
    def get(self, request):
        return render(request, "homepage.html")