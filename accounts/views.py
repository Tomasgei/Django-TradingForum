from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import  PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import login as auth_login
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

from .forms import SignUpForm

# Create your views here.

def SignUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)    
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect("home")
    else:
        form = SignUpForm()

    context = {"form":form}
    return render(request,"registrations/sign_up_new.html",context )


def PasswordResetRequest(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template = "registration/password_reset_email.txt"
                    c = {
                    "email": user.email,
                    "domain": "127.0.0.1:8000",
                    "site_name": "My Trading Forum",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token":  default_token_generator.make_token(user),
                    "protocol": "http",
                    }
                    email = render_to_string(email_template, c)
                    try:
                        send_mail(subject, email, "admin@tradingforum.com",[user.email],fail_silently=True )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("done/")
    form = PasswordResetForm()
    context = {"form": form}
    return render(request, '../templates/registrations/password_reset.html',context)    
