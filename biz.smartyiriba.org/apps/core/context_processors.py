from django.conf import settings

def business_contact(request):
    return {'business_contact': settings.BUSINESS_CONTACT}
