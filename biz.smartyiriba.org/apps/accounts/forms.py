from django.contrib.auth.forms import UserCreationForm
from .models import User
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'customer_type', 'organization', 'phone')
        labels = {'email': 'Adresse e-mail', 'customer_type': 'Type de client', 'organization': 'Organisation', 'phone': 'Téléphone'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
