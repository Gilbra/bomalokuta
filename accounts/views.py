# accounts/views.py
import uuid
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

from accounts.forms import UserCreationForm, ProfileUpdateForm
from accounts.models import User
from bomalokuta.models import CustomUser

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_validation_token = str(uuid.uuid4())
            user.is_active = False  # Désactiver le compte jusqu'à validation de l'email
            user.save()
            validation_link = request.build_absolute_uri(
                reverse('verify_email', args=[user.email_validation_token])
            )
            send_mail(
                'Confirmez votre adresse email',
                f'Cliquez sur ce lien pour vérifier votre email: {validation_link}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Un email de confirmation vous a été envoyé.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    user = get_object_or_404(User, email_validation_token=token)
    user.is_active = True
    user.email_validation_token = ''  # Réinitialiser le token
    user.save()
    messages.success(request, 'Votre email a été confirmé avec succès. Vous pouvez maintenant vous connecter.')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profil', request.user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', args=[uid, token])
                )
                send_mail(
                    'Réinitialisation du mot de passe',
                    f'Utilisez ce lien pour réinitialiser votre mot de passe: {reset_link}',
                    'noreply@example.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Un email de réinitialisation a été envoyé.')
                return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Votre mot de passe a été réinitialisé.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Le lien de réinitialisation est invalide.')
        return redirect('password_reset')

def profile(request, username):
    # Trouver l'utilisateur Django correspondant
    user = get_object_or_404(User, username=username)
    
    # Récupérer son profil CustomUser (s'il existe)
    try:
        custom_user = user.custom_user  # Accès direct à la relation OneToOneField
    except CustomUser.DoesNotExist:
        custom_user = None  # Aucun profil personnalisé trouvé

    return render(request, 'accounts/profil.html', locals())

