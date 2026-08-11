from .admin import AdminView
from django.shortcuts import render, redirect

# Create your views here.
class DashboardView(AdminView):
    def get(self, request):
        context = self.get_context_data()
        context['page'] = 'statistics'
        if self.request.user.is_anonymous:
            return redirect('homepage')
        return render(request, "admin/dashboard.html", context=context)
