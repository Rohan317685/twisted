from .admin import AdminView
from django.shortcuts import render, redirect

# Create your views here.
class PathwaysView(AdminView):
    def get(self, request):
        context = self.get_context_data(page='pathways')
        return render(request, "admin/pathways.html", context=context)
