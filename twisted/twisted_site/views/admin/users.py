from django.http import HttpResponse
from .admin import AdminView
from django.shortcuts import render, redirect
from ...models import User, Profile
from django.db.models import Q

# Create your views here.
class UsersView(AdminView):
    def get(self, request):
        context = self.get_context_data()
        context['page'] = 'users'
        if request.GET.get('search'):
            query = request.GET['search']
            context['users'] = User.objects.all()
            context['users'] = User.objects.filter(
                Q(profile__slack_username__icontains=query) |
                Q(profile__slack_id__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).order_by('profile__slack_username')
            context['search'] = True
        else:
            context['users'] = User.objects.all().order_by('profile__slack_username')
        return render(request, "admin/users.html", context=context)