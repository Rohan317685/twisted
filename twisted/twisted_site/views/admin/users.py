from .admin import AdminView
from django.shortcuts import render, redirect

# Create your views here.
class UsersView(AdminView):
    def get(self, request):
        context = self.get_context_data()
        context['page'] = 'users'
        return render(request, "admin/users.html", context=context)
