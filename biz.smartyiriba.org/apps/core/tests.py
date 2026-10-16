from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.catalog.models import Category, Service
from apps.quotes.models import QuoteRequest

class BusinessFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Web', slug='web')
        cls.service = Service.objects.create(category=category, title='Site web', slug='site-web', description='Création de site', active=True)
        cls.hidden = Service.objects.create(category=category, title='Privé', slug='prive', description='Non publié')
        cls.owner = User.objects.create_user(username='owner', password='test-secure-password')
        cls.other = User.objects.create_user(username='other', password='test-secure-password')

    def test_public_catalog_hides_unpublished_services(self):
        response = self.client.get(reverse('services'))
        self.assertContains(response, 'Site web')
        self.assertNotContains(response, 'Privé')
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)

    def test_quote_is_bound_to_authenticated_customer(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse('quote'), {'name': 'Client', 'email': 'client@example.com', 'phone': '+22300000000', 'country': 'Mali', 'customer_type': 'business', 'service': self.service.pk, 'description': 'Notre nouveau site web', 'customer': self.other.pk, 'status': 'accepted'})
        self.assertRedirects(response, reverse('quote_success'))
        quote = QuoteRequest.objects.get()
        self.assertEqual(quote.customer, self.owner)
        self.assertEqual(quote.status, 'new')

    def test_dashboard_isolates_customer_data(self):
        quote = QuoteRequest.objects.create(customer=self.other, name='Autre', email='other@example.com', phone='123', country='Mali', customer_type='individual', service=self.service, description='Besoin privé')
        self.assertRedirects(self.client.get(reverse('dashboard')), reverse('login') + '?next=/compte/')
        self.client.force_login(self.owner)
        self.assertNotContains(self.client.get(reverse('dashboard')), str(quote.reference))

    def test_unpublished_service_cannot_receive_quote(self):
        response = self.client.post(reverse('quote'), {'name': 'Client', 'email': 'client@example.com', 'phone': '123', 'country': 'Mali', 'customer_type': 'individual', 'service': self.hidden.pk, 'description': 'Besoin'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(QuoteRequest.objects.exists())

    def test_quote_requires_csrf(self):
        from django.test import Client
        self.assertEqual(Client(enforce_csrf_checks=True).post(reverse('quote'), {}).status_code, 403)
