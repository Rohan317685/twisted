from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from ...models import Pathway


# Create your views here.
class PathwaysView(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect("homepage")

        profile = request.user.profile
        pathways = Pathway.objects.order_by("start").all()
        pathways_reversed = Pathway.objects.order_by("-start").all()

        current_pathways = []
        for pathway in pathways:
            if not pathway.in_progress():
                continue
            minutes_spent = pathway.mins_spent(request.user)
            current_pathways.append(
                {
                    "pathway": pathway,
                    "minutes_spent": minutes_spent,
                    "unlocked": minutes_spent > pathway.min_mins,
                }
            )

        past_pathways = []
        for pathway in pathways_reversed:
            if not pathway.ended():
                continue
            minutes_spent = pathway.mins_spent(request.user)
            past_pathways.append(
                {
                    "pathway": pathway,
                    "minutes_spent": minutes_spent,
                    "unlocked": minutes_spent > pathway.min_mins,
                }
            )

        future_pathways = []
        for pathway in pathways:
            if not pathway.didnt_start():
                continue
            minutes_spent = 0
            future_pathways.append(
                {
                    "pathway": pathway,
                    "minutes_spent": minutes_spent,
                    "unlocked": minutes_spent > pathway.min_mins,
                }
            )

        return render(
            request,
            "client/pathways.html",
            {
                "profile": profile,
                "pathways": pathways,
                "current_pathways": current_pathways,
                "past_pathways": past_pathways,
                "future_pathways": future_pathways,
            },
        )
