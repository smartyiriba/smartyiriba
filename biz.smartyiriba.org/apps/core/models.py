from django.db import models
class ContactMessage(models.Model):
    name = models.CharField('Nom complet', max_length=180)
    email = models.EmailField('Email')
    phone = models.CharField('Téléphone', max_length=40, blank=True)
    organization = models.CharField('Organisation', max_length=200, blank=True)
    subject = models.CharField('Objet', max_length=200)
    message = models.TextField('Votre message', max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField('Traité', default=False)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'message de contact'
    def __str__(self): return self.subject

class ShowcaseEntry(models.Model):
    class Kind(models.TextChoices):
        PROJECT = 'project', 'Réalisation'
        CLIENT = 'client', 'Client / partenaire commercial autorisé'
        TEAM = 'team', 'Équipe professionnelle'
        OPPORTUNITY = 'opportunity', 'Opportunité commerciale'
        LEGAL = 'legal', 'Document légal ou commercial'
    kind = models.CharField('Rubrique', max_length=20, choices=Kind.choices)
    title = models.CharField('Titre', max_length=200)
    description = models.TextField('Description')
    link = models.URLField('Lien public', blank=True)
    published = models.BooleanField('Publication autorisée', default=False)
    position = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['position', 'title']
        verbose_name = 'contenu vitrine'
    def __str__(self): return self.title

class TrainingSession(models.Model):
    title = models.CharField('Titre', max_length=180)
    description = models.TextField('Programme et objectifs')
    audience = models.CharField('Public et prérequis', max_length=250)
    format = models.CharField('Format', max_length=180)
    date = models.DateField('Date de début', null=True, blank=True)
    duration = models.CharField('Durée', max_length=100)
    seats = models.PositiveIntegerField('Places', null=True, blank=True)
    price = models.DecimalField('Prix FCFA (vide : sur devis)', max_digits=12, decimal_places=0, null=True, blank=True)
    certificate = models.CharField('Attestation ou certificat éventuel', max_length=200, blank=True)
    conditions = models.TextField("Conditions d'inscription", blank=True)
    program = models.BooleanField('Programme / cohorte', default=False)
    published = models.BooleanField('Publié', default=False)
    class Meta:
        ordering = ['date', 'title']
        constraints = [models.CheckConstraint(condition=models.Q(price__isnull=True) | models.Q(price__gte=0), name='training_nonnegative_price'), models.CheckConstraint(condition=models.Q(seats__isnull=True) | models.Q(seats__gt=0), name='training_positive_seats')]
        verbose_name = 'session de formation'
    def __str__(self): return self.title
