"""
# main_app/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from main_app.models import Policy

class Command(BaseCommand):
    help = 'Send reminders for upcoming premium payments'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        policies = Policy.objects.filter(end_date__gte=today)

        for policy in policies:
            # Logic to send reminder (e.g., send email)
            self.stdout.write(f'Reminder sent for policy {policy.policy_number}')

        self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.management.base import BaseCommand
from django.utils import timezone
from main_app.models import Policy

# SMTP server configuration
SMTP_SERVER = 'smtp.your_email_provider.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'

# Sender information
SENDER_EMAIL = 'your_email@example.com'
SENDER_NAME = 'Your Name or Company'

# Reminder email content
SUBJECT = 'Insurance Payment Reminder'
BODY_TEMPLATE = """
Dear {name},

This is a friendly reminder that your insurance payment for policy {policy_number} is due on {due_date}.

Thank you for your attention.

Best regards,
{sender_name}
"""

def send_reminder(policy):
    client_email = policy.user.email  # Assuming the User model has an email field
    client_name = policy.user.username  # Assuming username is used for the name
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = client_email
    msg['Subject'] = SUBJECT
    
    body = BODY_TEMPLATE.format(name=client_name, policy_number=policy.policy_number, due_date=policy.end_date, sender_name=SENDER_NAME)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, client_email, msg.as_string())
        server.quit()
        print(f"Reminder sent to {client_name} at {client_email}")
    except Exception as e:
        print(f"Failed to send email to {client_name}. Error: {str(e)}")

class Command(BaseCommand):
    help = 'Send reminders for upcoming premium payments'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        policies = Policy.objects.filter(end_date__gte=today)

        for policy in policies:
            send_reminder(policy)
            self.stdout.write(f'Reminder sent for policy {policy.policy_number}')

        self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))
