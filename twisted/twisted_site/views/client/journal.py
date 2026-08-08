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
        context["info"] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")

        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.hackatime_time_unjournaled()

        log_minutes = min(log_minutes, HACKATIME_MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes

        return render(
            request, "client/projects/journal/new_hackatime.html", context=context
        )

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")

        reduced_minutes = min(
            project.hackatime_time_unjournaled(), HACKATIME_MAX_LOGGABLE_MINUTES
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

        journal = Journal(
            project=project,
            type="hackatime",
            content=content,
            minutes_worked=project.hackatime_time_unjournaled(),
            reduced_minutes=reduced_minutes,
        )
        journal.save()

        return self.get(request, id, context={"success": True})


UNTRACKED_MAX_LOGGABLE_MINUTES = 180

class NewProjectUntrackedJournal(View):
    def get(self, request, id, info=None, context={}):
        context["info"] = info
        if self.request.user.is_anonymous:
            return redirect("homepage")
        
        project = Project.objects.get(id=id)

        if project.project_type == 'software':
            return redirect('fr.projects.journals.new.hackatime')
        
        if project.user != request.user:
            return redirect("dashboard")

        context["project"] = project

        log_minutes = project.hackatime_time_unjournaled()

        log_minutes = min(log_minutes, HACKATIME_MAX_LOGGABLE_MINUTES)

        context["log_minutes"] = log_minutes

        context["max_mins"] = UNTRACKED_MAX_LOGGABLE_MINUTES

        context["info"] = (
            "logging untracked journals is generally not advised. time deflation may occur."
        )

        return render(
            request, "client/projects/journal/new_untracked.html", context=context
        )

    def post(self, request, id):
        project = Project.objects.get(id=id)
        if project.user != request.user:
            return redirect("dashboard")
        
        if project.project_type == 'software':
            return redirect('fr.projects.journals.new.hackatime')

        content = request.POST["content"]
        time_logged = int(request.POST["time_logged"])

        if time_logged > 180:
            return self.get(
                request,
                id,
                info="Time logged cannot be more than 180 minutes!",
                context={"content": content},
            )

        if len(content) < min(100, time_logged * 2):
            return self.get(
                request,
                id,
                info=f"Content length must be more than 120 characters per hour!<br>({len(content)} of {time_logged} required)",
                context={"content": content},
            )

        journal = Journal(
            project=project,
            type="untracked",
            content=content,
            minutes_worked=time_logged,
            reduced_minutes=time_logged,
        )
        journal.save()

        return self.get(request, id, context={"success": True})

class DeleteJournal(View):
    def get(self, request, id, context={'success': False}):
        if request.user.is_anonymous:
            return redirect('homepage')
        
        if id is not None:
            journal = Journal.objects.get(id=id)
            if journal.project.user != request.user:
                return redirect('dashboard')
            
            if journal.type != 'untracked':
                return redirect('dashboard')
            
            
            context['journal'] = journal
        
        return render(
            request, "client/projects/journal/delete.html", context=context
        )

    def post(self, request, id):
        if request.user.is_anonymous:
            return redirect('homepage')
        print('hi', flush=True)
        
        journal = Journal.objects.get(id=id)
        print(journal)
        
        if journal.project.user != request.user:
            return redirect('dashboard')
        
        if journal.type != 'untracked':
            return redirect('dashboard')
        
        journal.delete()
        
        
        return self.get(request, id=None, context={"success": True})
