""" helper function for the operation"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def send_verification_email(request, user, subject):
    """ it will send the verification email to verify their user account"""
    sub_match = {
        'RP': ('Password Reset', 'accounts/emails/reset_password_email.html'),
        'AA': ('Account Activation', 'accounts/emails/account_verification_email.html')
    }

    site = get_current_site(request)
    mail_subject = sub_match[subject][0]
    message = render_to_string(sub_match[subject][1], {
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
