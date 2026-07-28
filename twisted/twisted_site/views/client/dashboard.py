from django.views import View
from django.shortcuts import render

# Create your views here.
class DashboardView(View):
    def get(self, request):
        profile = self.request.user.profile
        return render(request, "client/dashboard.html", {
            "profile": profile
        })