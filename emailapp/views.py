from django.shortcuts import render,redirect
from django.http import HttpResponse
from emailapp.forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from emailapp.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth import login, logout, authenticate

# Create your views here.




def register(request):
  if request.method == 'POST':
    register_form=RegForm(request.POST, request.FILES)
    if register_form.is_valid():
      user = register_form.save()
      user.refresh_from_db()
      user.profile.first_name = register_form.cleaned_data.get('first_name')
      user.profile.last_name = register_form.cleaned_data.get('last_name')
      user.profile.email = register_form.cleaned_data.get('email')
      user.profile.phone = register_form.cleaned_data.get('phone')
      
  # user can't login until link confirmed
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      subject = 'Please Activate Your Account'
      # load a template like get_template()
      # and calls its render() method immediately.
      message = render_to_string('emailapp/activation_request.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # method will generate a hash value with user related data
        'token': account_activation_token.make_token(user),
      })
      user.email_user(subject, message)
      return redirect('activation_sent')

      # messages.success(request, 'User Registered')
  else:
       register_form=RegForm()
  return render(request,'emailapp/register.html',{'reg': register_form})


def sent(request):
  return render(request,'emailapp/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('emailapp:login')
    else:
        return render(request, 'emailapp/account_invalid.html')
      
      
      
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('emailapp:dashboard')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'emailapp/login.html')
  
  
def dashboard(request):
  return render(request,'emailapp/dashboard.html')

  
