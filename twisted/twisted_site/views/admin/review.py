from .admin import AdminView
from django.shortcuts import render, redirect

# Create your views here.
class ReviewView(AdminView):
    def get(self, request):
        context = self.get_context_data(page='review')
        return render(request, "admin/review.html", context=context)
