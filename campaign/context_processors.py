#COTNEXT PROCESSOR
from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_MOTO': settings.SITE_MOTO,
        'SITE_DESCRIPTION':settings.SITE_DESCRIPTION
    }
