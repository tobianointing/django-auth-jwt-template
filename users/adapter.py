from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        otp = self.generate_security_code()
        emailconfirmation.key = otp

        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "otp": otp,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation_message"

        emailconfirmation.save()
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def generate_security_code(self):
        """
        Returns a unique random `security_code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")
