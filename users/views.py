from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
# from products.models import Basket
from users.models import EmailVerification, User


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')


class UserRegistrationCreateView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'Store - Регистрация'


class UserProfileUpdateView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileUpdateView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной поты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_veryfied_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
