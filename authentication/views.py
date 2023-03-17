# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.encoding import force_str, force_bytes
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
import threading
from . import forms


User = get_user_model()

# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class CustomRegisterView(CreateView):
    """_summary_

    Args:
        CustomRegisterView (_type_): 'Registration View'
    """
    template_name = 'authentication/register.html'
    redirect_authenticated_user = True
    form_class = forms.CustomRegistrationForm
    success_url = reverse_lazy('authentication:chat_login')

    def get_success_url(self):
        return super().get_success_url()

    # def post(self, *args, **kwargs):
    #     # print('here')
    #     form = self.form_class(self.request.POST)
    #     if form.is_valid:
    #         return print(form)
    #     return super(CustomRegisterView, self).post(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super(CustomRegisterView, self).get(*args, **kwargs)


class EmailVerification(View):
    success_url = reverse_lazy('authentication:chat_login')
    redirect_url = reverse_lazy('authentication:chat_register')
    home_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # print(kwargs['token'])
        # print(kwargs.uuid)
        if kwargs.get('uuid', None) and kwargs.get('token', None):
            try:

                uid = kwargs.get('uuid')
                user = User.objects.get(uid=uid)

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

                return redirect(self.redirect_url)

            if user is not None and account_activation_token.check_token(user, token=kwargs.get('token')):
                user.is_active = True
                user.save()
                return redirect(self.success_url)
            else:
                current_site = get_current_site(request)
                # print('Second Resending Create')

                forms.SendEmail(
                    user=user,
                    domain=current_site.domain,
                    uuid=force_str(user.uid),
                    token=account_activation_token.make_token(user),
                ).start_process()

                # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
                # return HttpResponse('Resending Activation link Sent!')
                return redirect(self.home_url)


class CustomLoginView(LoginView):
    """_summary_

    Args:
        CustomLoginView (_type_): 'Login View'
    """

    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    form_class = forms.CustomAuthenticationForm
    success_url = reverse_lazy('chat:index')

    def get_success_url(self):
        return super().get_success_url()

    def form_invalid(self, form):
        # print('form invalid')
        send_to = form.cleaned_data['username']
        current_site = get_current_site(self.request)
        user = User.objects.get(email=send_to)
        
        # print('Second Resending Create')

        forms.SendEmail(
            user=user,
            domain=current_site.domain,
            uuid=force_str(user.uid),
            token=account_activation_token.make_token(user),
        ).start_process()
        return super().form_invalid(form)


class CustomAuthLogout(LoginRequiredMixin, LogoutView):
    '''
        For Logging out users
    '''
    next_page = 'authentication:chat_login'
