from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from ...models import Profile, Project
from ... import hackatime

# Create your views here.
class ProjectDetail(View):
    def get(self, request, id):
        if self.request.user.is_anonymous:
            return redirect('homepage')
        
        context = {}
        
        profile: Profile = request.user.profile
        context['profile'] = profile

        project = Project.objects.get(id=id)
        context['project'] = project
        
        if project.user == request.user:
            context['owner'] = True
        else:
            context['owner'] = False
        
        
        return render(
            request,
            "client/projects/detail.html",
            context,
        )

class ProjectSettings(View):
    def get(self, request, id):
        if self.request.user.is_anonymous:
            return redirect('homepage')
        
        context = {}

        project = Project.objects.get(id=id)
        context['project'] = project
        
        if project.user != request.user:
            return redirect('dashboard')
        
        profile = request.user.profile
        context['profile'] = profile
        
        context['hackatime_projects'] = hackatime.projects(profile.hackatime_access_token)
        
        return render(
            request,
            "client/projects/settings.html",
            context,
        )
    
    def post(self, request, id):
        if self.request.user.is_anonymous:
            return redirect('homepage')
        
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect('dashboard')
        
        project.project_name = request.POST['name']
        project.project_description = request.POST['description']
        project.project_type = request.POST['type']
        project.hackatime_project_name = request.POST['hackatime']
        project.save()
        return redirect('fr.projects.detail', project.id)