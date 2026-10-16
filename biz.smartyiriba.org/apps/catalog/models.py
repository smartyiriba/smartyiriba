from django.db import models
from django.urls import reverse
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = 'catégories'
    def __str__(self): return self.name
class Service(models.Model):
    class Pricing(models.TextChoices):
        FIXED = 'fixed', 'Prix fixe'
        FROM = 'from', 'À partir de'
        QUOTE = 'quote', 'Sur devis'
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    audience = models.TextField(blank=True)
    features = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    estimated_delivery = models.CharField(max_length=160, blank=True)
    conditions = models.TextField(blank=True)
    faq = models.TextField(blank=True)
    pricing = models.CharField(max_length=10, choices=Pricing.choices, default=Pricing.QUOTE)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=[('XOF', 'FCFA'), ('EUR', 'EUR'), ('USD', 'USD')], default='XOF')
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['title']
        constraints = [models.CheckConstraint(condition=models.Q(price__gte=0) | models.Q(price__isnull=True), name='service_nonnegative_price'), models.CheckConstraint(condition=models.Q(pricing='quote') | models.Q(price__isnull=False), name='service_requires_price')]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse('service_detail', args=[self.slug])
