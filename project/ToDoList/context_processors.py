# core/context_processors.py

from django.conf import settings
from .models import *  # Import your SystemSettings model here



def unread_notifications_count(request):
    if request.user.is_authenticated:
        return {'unread_notifications_count': request.user.received_notifications.filter(is_read=False).count()}
    return {'unread_notifications_count': 0}

def system_settings(request):
    try:
        system_settings = SystemSettings.objects.first()  # Fetch your SystemSettings object
        company_logo_url = None
        small_logo_url = None
        
        if system_settings:
            if system_settings.company_logo:
                company_logo_url = settings.MEDIA_URL + system_settings.company_logo
            if system_settings.small_logo:
                small_logo_url = settings.MEDIA_URL + system_settings.small_logo
                
    except SystemSettings.DoesNotExist:
        system_settings = None
        company_logo_url = None
        small_logo_url = None

    return {
        'system_settings': system_settings,
        'company_logo_url': company_logo_url,
        'small_logo_url': small_logo_url,
    }
