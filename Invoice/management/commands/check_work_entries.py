from django.core.management.base import BaseCommand
from Invoice.models import WorkEntry, User, ClientProject, Category
from django.utils import timezone

class Command(BaseCommand):
    help = 'Check work entries in the database'

    def handle(self, *args, **options):
        # Check users
        users = User.objects.filter(role='user')
        self.stdout.write(f"\nUsers found: {users.count()}")
        for user in users:
            self.stdout.write(f"User: {user.username}, Managed by: {user.managed_by}")
            
        # Check projects
        projects = ClientProject.objects.all()
        self.stdout.write(f"\nProjects found: {projects.count()}")
        for project in projects:
            self.stdout.write(f"Project: {project.name}, Managed by: {project.managed_by}")
            
        # Check categories
        categories = Category.objects.all()
        self.stdout.write(f"\nCategories found: {categories.count()}")
        for category in categories:
            self.stdout.write(f"Category: {category.name}, Project: {category.project.name}")
            
        # Check work entries from last 24 hours
        recent_entries = WorkEntry.objects.filter(
            date__gte=timezone.now() - timezone.timedelta(days=1)
        ).select_related('user', 'project', 'category')
        
        self.stdout.write(f"\nRecent work entries (last 24h): {recent_entries.count()}")
        for entry in recent_entries:
            self.stdout.write(
                f"Entry: User={entry.user.username if entry.user else 'None'}, "
                f"Project={entry.project.name if entry.project else 'None'}, "
                f"Category={entry.category.name if entry.category else 'None'}, "
                f"Folder={entry.folder_name}, "
                f"Date={entry.date}"
            )
