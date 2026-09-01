from django.template.response import TemplateResponse
from .admin import AdminView
from django.shortcuts import render, redirect
from ...models import AuditLog

# Create your views here.
class AuditLogsView(AdminView):
    def get(self, request):
        context = self.get_context_data(page='logs')
        context['logs'] = AuditLog.objects.order_by('-timestamp').all()
        return TemplateResponse(request, "admin/logs.html", context=context)
