from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group

from users_core.forms import SignUpForm
from users_core.tokens import account_activation_token

@login_required
def home(request):
    return redirect('/')


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Attiva il tuo account su ELSA GEST'
            message = render_to_string('elsausers/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # in realtà non manda un emerito cazzo! TODO
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'elsausers/useradd.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'elsausers/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        group = Group.objects.get(name='premium')
        group.user_set.add(user)
        login(request, user)
        return redirect("/")
    else:
        return render(request, 'elsausers/account_activation_invalid.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password modificata con successo!')
            return redirect('/')
        else:
            messages.error(request, 'Per favore correggi gli errori')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'elsausers/change_password.html', {
        'form': form
    })
