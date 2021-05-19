from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout,login,authenticate
from django.db.models import Q,Sum
from .models import User
from .decorators import is_estate_manager,is_landord,is_tenant
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
from django.db.models import Sum
from django.core.mail import send_mail
from registration.views import RegistrationView
from registration.models import RegistrationProfile
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from registration import signals
from django.utils import timezone
from decimal import Decimal
import requests
from django.contrib.auth import views as auth_views


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR','')
    if x_forwarded_for:
        ip = x_forwarded_for
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RegisterView(RegistrationView):

    success_url = 'registration_complete'
    registration_profile = RegistrationProfile
    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)

    def __country_name(self):
        ip_address = get_client_ip(self.request)
        post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
        response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
        geodata = response.json()
        return geodata['country_name']
    def __country_code(self):
        ip_address = get_client_ip(self.request)
        post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
        response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
        geodata = response.json()
        return geodata['country_code']
    def __ip_address(self):
        ip_address = get_client_ip(self.request)
        post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
        response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
        geodata = response.json()
        return geodata['ip']
    def __state(self):
        ip_address = get_client_ip(self.request)
        post_data = {'access_key': 'ad3006e4508bb76ba1b6b0d7978ba5ac'}
        response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
        geodata = response.json()
        return geodata['city']

    def register(self, form):
        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save(commit=False)
            print(new_user_instance)
            new_user_instance.country = self.__country_name()
            new_user_instance.country_short = self.__country_code()
            new_user_instance.ip_address = self.__ip_address()
            new_user_instance.state = self.__state()
            if new_user_instance.gender == 'M':
                new_user_instance.image = 'images/male.png'
            elif new_user_instance.gender == 'F':
                new_user_instance.image = 'images/female.png'
            new_user_instance.save()
        else:
            new_user_instance = (User.objects.create_user(**form.cleaned_data))

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user


def login_view(request):
    site_title = 'Login Page'
    my_val = {'title': site_title}
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.role == 1:
                    return redirect('index')
                elif user.role == 2:
                    return redirect('index')
                elif user.role == 3:
                    return redirect('index')

    return render(request, 'login.html', context=my_val)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/accounts/login')


def test(request):
    # IP LOCATIN FINDER
    # ip_address = get_client_ip(request)
    # post_data = {'access_key':'ad3006e4508bb76ba1b6b0d7978ba5ac'}
    # response = requests.get('http://api.ipstack.com/{}'.format(ip_address), params=post_data)
    # geodata = response.json()
    # print(geodata)
    #
    # url = 'https://api.mybitx.com/api/1/balance'
    # resp = requests.get(url=url, auth=(settings.KEY_ID,settings.KEY_SECRET))
    # balance = resp.json()
    # extra_b = balance['balance'][2]

    try:
        url = 'https://api.mybitx.com/api/1/funding_address'
        data = {'asset': 'XBT'}
        respd = requests.post(url=url, data=data, auth=(settings.KEY_ID, settings.KEY_SECRET))
        bal = respd.json()
        wallet_address = bal['address']
        print(wallet_address)
    except:
        wallet_address ='36TSMVe7VpNWHaPx4ZcZTcnuYB83VWhaYC'
        print(wallet_address)



    return render(request, 'site/test.html')
