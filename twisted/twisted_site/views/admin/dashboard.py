from django.views import View
from django.shortcuts import render, redirect

# Create your views here.
class DashboardView(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect('homepage')
        profile = self.request.user.profile
        return render(request, "admin/dashboard.html", {
            "profile": profile
        })
