from django import forms
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    consent = forms.BooleanField(label='J’accepte que mes coordonnées soient utilisées pour répondre à cette demande.')
    website = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'phone', 'organization', 'subject', 'message')
        labels = {'email': 'Adresse e-mail'}
    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Envoi non valide.')
        return ''
