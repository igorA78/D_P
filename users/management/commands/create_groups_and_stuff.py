from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        moderator_group = Group.objects.create(name='moderator')
        moderator_group.permissions.add(
            Permission.objects.filter(codename='moderator').first()
        )
        moderator_group.save()

        content_manager_group = Group.objects.create(name='content_manager')
        content_manager_group.permissions.add(
            Permission.objects.filter(codename='content_manager').first()
        )
        content_manager_group.save()

        moderator = User.objects.create(
            email='moderator@email.com',
            first_name='moderator',
            last_name='moderator',
        )
        moderator.set_password('12345')
        moderator.groups.add(moderator_group)
        moderator.save()

        content_manager = User.objects.create(
            email='content_manager@email.com',
            first_name='content_manager',
            last_name='content_manager',
        )
        content_manager.set_password('12345')
        content_manager.groups.add(content_manager_group)
        content_manager.save()
