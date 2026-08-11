from django.template.loader import render_to_string
from django.conf import settings
import os
from django.core.mail import send_mail
try:
    from weasyprint import HTML
except Exception:
    HTML = None

def generate_exit_pass_pdf(permission):
    if HTML is None:
        # WeasyPrint not installed; skip PDF generation
        return None
    html_string = render_to_string('school/exit_pass.html', {'permission': permission})
    out_dir = os.path.join(settings.MEDIA_ROOT, 'exit_passes')
    os.makedirs(out_dir, exist_ok=True)
    filename = f"exit_pass_{permission.id}.pdf"
    full_path = os.path.join(out_dir, filename)
    HTML(string=html_string).write_pdf(full_path)
    return os.path.join('exit_passes', filename)

def notify_parent_on_status_change(permission):
    parent = permission.student.parent
    subject = f"Permission {permission.status.capitalize()} for {permission.student.name}"
    message = f"Hello {parent.name},\n\nThe permission request for student {permission.student.name} ({permission.student.reg_number}) is now: {permission.status}.\n\nNote: {permission.note}\n"
    if permission.status == 'approved' and permission.exit_pass:
        download_url = f"{settings.SITE_URL}{permission.get_download_url()}" if settings.SITE_URL else None
        if download_url:
            message += f"\nDownload exit pass: {download_url}\n"
    # Send email (console backend in dev)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [parent.email], fail_silently=True)

    # Optionally send SMS via Twilio
    if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_FROM_NUMBER:
        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            sms = f"{permission.student.name}: permission {permission.status}."
            if permission.status == 'approved' and permission.exit_pass and settings.SITE_URL:
                sms += f" Exit pass: {settings.SITE_URL}{permission.get_download_url()}"
            client.messages.create(body=sms, from_=settings.TWILIO_FROM_NUMBER, to=parent.phone)
        except Exception as e:
            # In production log this
            pass
