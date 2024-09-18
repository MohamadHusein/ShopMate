from django.shortcuts import render , redirect ,reverse
from django.views import View
from .forms import LoginForm, OtpLoginForm , CheckOtpForm , AddressCreationForm
from django.contrib.auth import authenticate, login, logout
from random import randint
from account.models import Otp , User
from django.utils.crypto import get_random_string
from uuid import uuid4
import requests
import json


url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS"






class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})



    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                form.add_error('phone' , 'invalid user data')
        else:
            form.add_error('phone' , 'invalid  data')

        return render(request, 'account/login.html', {'form': form})





class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'account/otp_login.html', {'form': form})



    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            ghasedak = randint(1000 , 9999)
            cd = form.cleaned_data
            payload = json.dumps({
                "sendDate": "2024-07-04T07:41:15.992Z",
                "receptors": [
                    {
                        cd['phone']
                    }
                ],
                "templateName": "Ghasedak",
                "inputs": [
                    {
                        "param": ghasedak
                    }
                ],
                "udh": True
            })
            headers = {
                'Content-Type': 'application/json',
                'ApiKey': 'your-apiKey'
            }
            token =  str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=ghasedak ,  token=token)


            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            return redirect(reverse('account:check_otp') + f'?token{token}')
        else:
            form.add_error('phone' , 'invalid  data')

        return render(request, 'account/otp_login.html', {'form': form})








class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})


    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            ghasedak = randint(1000 , 9999)
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'] , token=token).exists():
                otp = Otp.objects.get(token=token)
                user , is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user , backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
        else:
            form.add_error('phone' , 'invalid  data')

        return render(request, 'account/check_otp.html', {'form': form})




class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})









def user_logout(request):
    logout(request)
    return redirect('/')


























