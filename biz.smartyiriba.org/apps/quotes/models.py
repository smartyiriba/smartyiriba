import uuid
from django.conf import settings
from django.db import models
class QuoteRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Nouveau'
        REVIEW = 'review', 'En analyse'
        INFORMATION = 'information', 'Informations requises'
        PREPARED = 'prepared', 'Devis préparé'
        SENT = 'sent', 'Envoyé'
        ACCEPTED = 'accepted', 'Accepté'
        DECLINED = 'declined', 'Refusé'
        EXPIRED = 'expired', 'Expiré'
        CONVERTED = 'converted', 'Converti en commande'
    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=180)
    organization = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    country = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=20, choices=[('individual', 'Particulier'), ('business', 'Entreprise'), ('ngo', 'ONG / Association'), ('institution', 'Institution')])
    service = models.ForeignKey('catalog.Service', on_delete=models.PROTECT)
    budget = models.CharField(max_length=160, blank=True)
    desired_deadline = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=10000)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return str(self.reference)
