from django import forms
from .models import QuoteRequest
from apps.catalog.models import Service
class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ('name', 'organization', 'email', 'phone', 'country', 'customer_type', 'service', 'budget', 'desired_deadline', 'description')
        labels = {'email': 'Adresse e-mail', 'service': 'Prestation recherchée', 'name': 'Nom complet', 'organization': 'Organisation', 'phone': 'Téléphone', 'country': 'Pays', 'customer_type': 'Type de client', 'budget': 'Budget indicatif', 'desired_deadline': 'Date souhaitée', 'description': 'Votre besoin'}
        widgets = {'desired_deadline': forms.DateInput(attrs={'type': 'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(active=True)
