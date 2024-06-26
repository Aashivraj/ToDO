# core/context_processors.py

from django.conf import settings
from .models import SystemSettings  # Import your SystemSettings model here

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
