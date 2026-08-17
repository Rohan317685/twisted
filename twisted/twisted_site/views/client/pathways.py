from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from ...models import Pathway


# Create your views here.
class PathwaysView(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect('homepage')
        
        profile = request.user.profile
        pathways = Pathway.objects.order_by('-start').all()

        current_pathway = None
        for pathway in pathways:
            if pathway.start < timezone.now() and pathway.end > timezone.now():
                current_pathway = pathway
                break
        
        return render(
            request,
            "client/pathways.html",
            {"profile": profile, 'pathways': pathways, "current_pathway": current_pathway},
        )
