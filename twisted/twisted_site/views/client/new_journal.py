from markdown_it.rules_inline import image
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from ...models import Profile, Project, Journal
from ... import hackatime
import re
import math

HACKATIME_MAX_LOGGABLE_MINUTES = 6 * 60

class NewProjectHackatimeJournal(View):
    def get(self, request, id, info=None, context={}):
        context['info'] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.time_unjournaled()

        log_minutes = min(log_minutes, HACKATIME_MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes

        return render(request, "client/projects/journal/new_hackatime.html", context=context)

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        reduced_minutes = min(
            project.time_unjournaled(), HACKATIME_MAX_LOGGABLE_MINUTES
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
            request, "client/projects/new_hackatime.html", context={"success": True}
        )

class NewProjectLookoutJournal(View):
    def get(self, request, id, info=None, context={}):
        context['info'] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.time_unjournaled()

        log_minutes = min(log_minutes, HACKATIME_MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes
        
        context['info'] = "TODO: This has NOT been implemented yet."

        return render(request, "client/projects/journal/new_lookout.html", context=context)

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        reduced_minutes = min(
            project.time_unjournaled(), HACKATIME_MAX_LOGGABLE_MINUTES
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
            request, "client/projects/new_lookout.html", context={"success": True}
        )

UNTRACKED_MAX_LOGGABLE_MINUTES = 120

class NewProjectUntrackedJournal(View):
    def get(self, request, id, info=None, context={}):
        context['info'] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.time_unjournaled()

        log_minutes = min(log_minutes, HACKATIME_MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes

        context['max_mins'] = UNTRACKED_MAX_LOGGABLE_MINUTES
        
        context['info'] = "logging untracked journals is generally not advised. time deflation may occur."
        
        return render(request, "client/projects/journal/new_untracked.html", context=context)

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        reduced_minutes = min(
            project.time_unjournaled(), HACKATIME_MAX_LOGGABLE_MINUTES
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
            request, "client/projects/new_untracked.html", context={"success": True}
        )
