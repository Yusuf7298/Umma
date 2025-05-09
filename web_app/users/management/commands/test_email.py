from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        send_mail(
            'Test Subject - Django Email',
            'This is a test email from your Django application.',
            None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            ['ym47484988@gmail.com'],  # Your receiving email
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS('Successfully sent test email!'))