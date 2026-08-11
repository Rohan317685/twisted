from django.views import View
from django.shortcuts import render, redirect, resolve_url
from dataclasses import dataclass

@dataclass
class SidebarLink:
    name: str
    icon: str
    text: str
    href: str

# Create your views here.
class AdminView(View):
    def get_context_data(self, **kwargs) -> dict:
        context = {}
        context["sidebar_links"] = [
            SidebarLink(name="dashboard", icon="analytics", text="Dashboard", href=resolve_url('admin.dash')),
            SidebarLink(name="users", icon="profile", text="Users", href=resolve_url('admin.users')),
            SidebarLink(name="pathways", icon="controls", text="Pathways", href=resolve_url('admin.pathways')),
            SidebarLink(name="fulfillment", icon="list", text="Fulfillment", href=resolve_url('admin.fulfillment')),
            SidebarLink(name="shop", icon="bag-add", text="Shop", href=resolve_url('admin.shop')),
            SidebarLink(name="review", icon="reply", text="Review", href=resolve_url('admin.review')),
            SidebarLink(name="announcements", icon="important", text="Announcements", href=resolve_url('admin.announcements')),
        ]
        context['profile'] = self.request.user.profile
        return context
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('homepage')
        if not request.user.profile.is_staff:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)