from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from ...models import Project


# Create your views here.
class ListProjects(View):
    def get(self, request):
        profile = request.user.profile

        projects = request.user.projects.all()

        return render(
            request,
            "client/projects/list.html",
            {"profile": profile, "projects": projects},
        )


class CreateProject(View):
    def get(self, request):
        profile = request.user.profile

        projects = request.user.projects.all()

        return render(
            request,
            "client/projects/create.html",
            {},
        )

    def post(self, request):
        project_name = request.POST["name"]
        project_description = request.POST["description"]
        project_type = request.POST["type"]

        Project.objects.create(
            user=request.user,
            project_name=project_name,
            project_description=project_description,
            project_type=project_type,
        )

        return render(
            request,
            "client/projects/create.html",
            {"complete": True},
        )
