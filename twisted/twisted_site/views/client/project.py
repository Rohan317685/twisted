from markdown_it.rules_inline import image
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from ...models import Profile, Project, Journal
from ... import hackatime
import re
import math

# Create your views here.
class ProjectDetail(View):
    def get(self, request, id):
        if self.request.user.is_anonymous:
            return redirect("homepage")

        context = {}

        profile: Profile = request.user.profile
        context["profile"] = profile

        project = Project.objects.get(id=id)
        context["project"] = project

        if project.user == request.user:
            context["owner"] = True
        else:
            context["owner"] = False

        return render(
            request,
            "client/projects/detail.html",
            context,
        )


class ProjectSettings(View):
    def get(self, request, id):
        if self.request.user.is_anonymous:
            return redirect("homepage")

        context = {}

        project = Project.objects.get(id=id)
        context["project"] = project

        if project.user != request.user:
            return redirect("dashboard")

        profile = request.user.profile
        context["profile"] = profile

        context["hackatime_projects"] = hackatime.projects(
            profile.hackatime_access_token
        )

        return render(
            request,
            "client/projects/settings.html",
            context,
        )

    def post(self, request, id):
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        project.project_name = request.POST["name"]
        project.project_description = request.POST["description"]
        project.project_type = request.POST["type"]
        project.hackatime_project_name = request.POST["hackatime"]
        project.save()
        return redirect("fr.projects.detail", project.id)


MAX_LOGGABLE_MINUTES = 6 * 60


class NewProjectJournal(View):
    def get(self, request, id, info=None, context={}):
        context['info'] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.time_unjournaled()

        log_minutes = min(log_minutes, MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes

        return render(request, "client/projects/journal.html", context=context)

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        reduced_minutes = min(
            project.time_unjournaled(), MAX_LOGGABLE_MINUTES
        )

        content = request.POST["content"]
        image_regex = r"\!\[.*?\]\(.*?\)"
        image_count = len(re.findall(image_regex, content))
        required_image_count = math.ceil(max(1, reduced_minutes / 180))

        if image_count < required_image_count:
            return self.get(
                request,
                id,
                info=f"please add atleast {required_image_count - image_count} more image(s) to log this journal!",
                context={"content": content},
            )
        if len(content) < min(100, reduced_minutes):
            return self.get(
                request,
                id,
                info=f"Content length must be more than 60 characters per hour!<br>({len(content)} of {reduced_minutes} required)",
                context={"content": content},
            )
        
        journal = Journal(project=project, content=content, minutes_worked = project.time_unjournaled(), reduced_minutes=reduced_minutes)
        journal.save()
        
        return render(
            request, "client/projects/journal.html", context={"success": True}
        )
