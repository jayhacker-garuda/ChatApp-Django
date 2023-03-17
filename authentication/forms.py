from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from django.conf import settings

from django.core.mail import EmailMessage
import threading

User = get_user_model()
# connection = get_connection()


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class SendEmail:
    """_summary_
    Args:
        SendMail (_type_): 'Send-Mail'
    """
    template_name = 'authentication/acc_active_email.html'
    mail_subject = 'Activation link has been sent to your email id'

    def __init__(self, user: object, domain: any, uuid: any, token: any):
        self.user = user
        self.domain = domain
        self.uuid = uuid
        self.token = token

    def start_process(self):

        message = render_to_string(self.template_name, {
            'user': self.user,
            'domain': self.domain,
            'uuid': self.uuid,
            'token': account_activation_token.make_token(self.user),
        })

        email = EmailMessage(
            self.mail_subject, message, 'no-reply@chatappaccounts.com', [
                self.user.email]
        )
        EmailThread(email).start()
        # pass


class CustomRegistrationForm(UserCreationForm):
    """_summary_

    Args:
        UserCreationForm (_type_): 'Create User Account'
    """

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:

            self.fields[field].widget.attrs.update({
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#fd913c] focus:border-[#fd913c] sm:text-sm'
            })
            self.fields[field].error_messages.update({
                'required': 'This %s fields is required' % field
            })

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        # current_site = get_current_site(self.request)
        # mail_subject = 'Activation link has been sent to your email id'
        # message = render_to_string('', {
        #     'user': user,
        #     'domain': '127.0.0.1:8000',
        #     'uid64': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })

        print('First Create')
        SendEmail(
            user=user,
            domain= settings.DEFAULT_DOMAIN,
            uuid=force_str(user.uid),
            token=account_activation_token.make_token(user),
        ).start_process()
        # email = EmailMessage(
        #     mail_subject, message, 'no-reply@chatappaccounts.com', [user.email]
        # )
        # EmailThread(email).start()
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """_summary_

    Args:
        AuthenticationForm (_type_): 'Logging In User'
    """

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#fd913c] focus:border-[#fd913c] sm:text-sm'
            })
            self.fields[field].error_messages.update({
                'required': 'This %s fields is required' % field
            })

    class Meta:
        model = User
        fields = ['email', 'password']
