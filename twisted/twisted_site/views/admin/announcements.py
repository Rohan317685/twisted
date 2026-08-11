from .admin import AdminView
from django.shortcuts import render, redirect

# Create your views here.
class AnnouncementsView(AdminView):
    def get(self, request):
        context = self.get_context_data()
        context['page'] = 'announcements'
        if self.request.user.is_anonymous:
            return redirect('homepage')
        return render(request, "admin/announcements.html", context=context)
