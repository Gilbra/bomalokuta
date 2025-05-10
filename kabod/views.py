# views.py

from django.utils import translation
from django.shortcuts import redirect

def home(request):
    return redirect ('bomalokuta:home')

def set_language(request):
    user_language = request.GET.get('language', 'fr')
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect(request.META.get('HTTP_REFERER', '/'))