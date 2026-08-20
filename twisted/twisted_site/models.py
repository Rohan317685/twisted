from django.db.models import TextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from . import hackatime

User = get_user_model()

JOURNAL_TYPES = {
    "hackatime": "Hackatime",
    "lookout": "Lookout",
    "untracked": "Untracked",
}


class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    link = models.CharField(max_length=500)
    cdn_response = models.JSONField()
    uploaded_thru = models.CharField(max_length=500)
    filesize = models.IntegerField()

    def __str__(self):
        return f"{self.cdn_response['filename']} uploaded by {self.uploaded_by.profile.slack_username}"


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verification_status = models.CharField(max_length=64, blank=True, default="")
    ysws_eligible = models.BooleanField(default=False)
    slack_id = models.CharField(max_length=64, blank=True, default="")
    slack_username = models.CharField(max_length=64, blank=True, default="")
    slack_pfp_url = models.CharField(max_length=200, blank=True, default="")

    hackatime_access_token = models.CharField(max_length=2000, blank=True, default="")
    hackatime_state = models.CharField(max_length=100, blank=True, default="")

    is_staff = models.BooleanField(default=False)
    is_allowed = models.BooleanField(default=False)

    def shipped_projects(self):
        shipped_projects = []
        for project in self.user.projects.all():
            if project.is_shipped():
                shipped_projects.append(project)
        return shipped_projects

    def time_logged(self):
        time_logged = 0
        for project in self.user.projects.all():
            time_logged += project.time_logged()
        return time_logged

    def time_shipped(self):
        time_shipped = 0
        for project in self.shipped_projects():
            time_shipped += project.time_logged()
        return time_shipped

    def __str__(self):
        return self.user.username  # ty:ignore[unresolved-attribute]


PROJECT_TYPE_CHOICES = {"software": "Software", "hardware": "Hardware"}


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="projects")

    project_name = models.CharField(max_length=50)
    project_description = models.TextField(max_length=2000)

    project_type = models.CharField(choices=PROJECT_TYPE_CHOICES, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hackatime_project_name = models.CharField(max_length=200, blank=True, default="")
    repo_url = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.project_name

    def get_hackatime_project(self) -> hackatime.HackatimeProject | None:
        if not self.hackatime_project_name:
            return
        projects = hackatime.projects(self.user.profile.hackatime_access_token)
        for project in projects:
            if project.name == self.hackatime_project_name:
                return project
        return

    def time_logged(self, include_all_minutes=False):
        minutes = 0
        for journal in self.journals.all():  # ty:ignore[unresolved-attribute]
            if include_all_minutes:
                # django-orm-lens-disable-next-line DOL007
                minutes += journal.minutes_worked
            else:
                minutes += journal.reduced_minutes
        return minutes

    def hackatime_logged(self, include_all_minutes=False):
        minutes = 0
        for journal in self.journals.all():  # ty:ignore[unresolved-attribute]
            if journal.type != "hackatime":
                continue
            if include_all_minutes:
                # django-orm-lens-disable-next-line DOL007
                minutes += journal.minutes_worked
            else:
                minutes += journal.reduced_minutes
        return minutes

    def time_spent(self):
        project = self.get_hackatime_project()
        if project is None:
            return 0
        return project.total_seconds // 60

    def hackatime_time_unjournaled(self):
        return self.time_spent() - self.hackatime_logged(include_all_minutes=True)

    def is_shipped(self):
        ships = ProjectShip.objects.filter(project=self)
        for ship in ships:
            if ship.status not in ["rejected", "requested_changes"]:
                return ship
        return False


class Journal(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, related_name="journals"
    )
    type = models.CharField(max_length=100, choices=JOURNAL_TYPES)

    content = TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    minutes_worked = models.IntegerField()
    reduced_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.reduced_minutes} mins on {self.project}"


PROJECT_SHIP_STATUSES = {
    "created": "Awaiting review",
    "rejected": "Rejected ship",
    "requested_changes": "Requested Changes",
    "reqchecked": "Checked by T1",
    "approved": "Approved by T2",
}


class ProjectShip(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="ships")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    t1_updated_at = models.DateTimeField(default=None, null=True)
    t2_updated_at = models.DateTimeField(default=None, null=True)

    t1_message = models.TextField(blank=True, default="")
    t2_message = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=200, choices=PROJECT_SHIP_STATUSES, default="created"
    )

    def __str__(self):
        return f"Ship created at {self.created_at} ({PROJECT_SHIP_STATUSES.get(str(self.status), self.status)})"


class Pathway(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    name = models.CharField(max_length=200)
    min_mins = models.IntegerField(default=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def ended(self):
        return timezone.now() > self.end

    def didnt_start(self):
        return self.start > timezone.now()

    def in_progress(self):
        return not self.ended() and not self.didnt_start()

    def mins_spent(self, user: User):
        pathways = Pathway.objects.order_by('start').values('id', 'start', 'end', 'min_mins')
        if not pathways:
            return 0
        
        pathway_totals = {p['id']: 0 for p in pathways}

        journals = Journal.objects.filter(
            project__user=user
        ).order_by('created_at').values_list('created_at', 'reduced_minutes')

        for j_created, j_mins in journals:
            mins_remaining = j_mins
            for pathway in pathways:
                if mins_remaining <= 0:
                    break
                
                # Check if journal falls within the pathway window
                if pathway['start'] > j_created or pathway['end'] < j_created:
                    continue
                
                p_id = pathway['id']
                mins_completed = pathway_totals.get(p_id, 0)
                mins_required = pathway['min_mins']

                if mins_completed >= mins_required:
                    continue

                mins_needed = mins_required - mins_completed
                mins_donated = min(j_mins, mins_needed)

                mins_remaining -= mins_donated
                pathway_totals[p_id] = mins_completed + mins_donated

        return pathway_totals.get(self.id, 0)

    def __str__(self):
        return self.name
