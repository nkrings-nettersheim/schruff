from django.conf import settings


def setting_enhancement(request):
    return {'PRODUCTION': settings.PRODUCTION}

