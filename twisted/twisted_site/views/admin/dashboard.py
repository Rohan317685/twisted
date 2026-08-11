from .admin import AdminView
from django.shortcuts import render, redirect
from ...models import Journal, Project, ProjectShip
import json
# Create your views here.
class DashboardView(AdminView):
    def get(self, request):
        context = self.get_context_data()
        context['page'] = 'dashboard'
        if self.request.user.is_anonymous:
            return redirect('homepage')
        hours_logged = 0
        hours_logged_chart = {}
        for journal in Journal.objects.all():
            hours = journal.reduced_minutes / 60
            hours_logged += hours
            date = journal.created_at.date().strftime("%a, %-d %b")
            hours_logged_chart[date] = hours_logged_chart.get(date, 0) + hours
        context['hours_logged_chart'] = json.dumps([['Date', 'Hours']] + list(hours_logged_chart.items()))
        
        context['hours_logged'] = round(hours_logged, 2)
        return render(request, "admin/dashboard.html", context=context)