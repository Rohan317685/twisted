from .admin import AdminView
from django.shortcuts import render, redirect
from ...models import Pathway

# Create your views here.
class PathwaysView(AdminView):
    def get(self, request):
        context = self.get_context_data(page='pathways')
        context['pathways'] = Pathway.objects.all().order_by('start')

        pathways = Pathway.objects.order_by("start").all()

        current_pathways = []
        past_pathways = []
        future_pathways = []
        
        for pathway in pathways:
            if pathway.in_progress():
                current_pathways.append(pathway)
            if pathway.ended():
                past_pathways.append(pathway)
            if pathway.didnt_start():
                future_pathways.append(pathway)

        past_pathways.reverse()        
        context['current_pathways'] = current_pathways
        context['past_pathways'] = past_pathways
        context['future_pathways'] = future_pathways
        
        return render(request, "admin/pathways.html", context=context)