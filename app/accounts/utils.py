""" helper function for the operation"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

SUB_MATCH = {
    'RP': ('Password Reset', 'accounts/emails/reset_password_email.html'),
    'AA': ('Account Activation', 'accounts/emails/account_verification_email.html'),
    'VA': ('Vendor Approval', 'accounts/emails/admin_approval_email.html'),
}


def send_verification_email(request, user, subject):
    """ it will send the verification email to verify their user account"""
    site = get_current_site(request)
    mail_subject = SUB_MATCH[subject][0]
    message = render_to_string(SUB_MATCH[subject][1], {
        'user': user,
        'domain': site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject,
                        message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[to_email]
                        )
    mail.send()


def send_notification(subject, context):
    """send notification to the vendor about the approval. """
    mail = EmailMessage(
        subject=SUB_MATCH[subject][0],
        body=render_to_string(SUB_MATCH[subject][1], context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[context['user'].email]
    )
    mail.send()
