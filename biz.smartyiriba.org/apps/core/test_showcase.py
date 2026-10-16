from datetime import timedelta
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.catalog.models import Service
from .models import ContactMessage, ShowcaseEntry, TrainingSession

class ShowcaseTests(TestCase):
    def setUp(self): cache.clear()

    def test_seed_is_idempotent_and_preserves_editor_changes(self):
        from io import StringIO
        call_command('seed_showcase', stdout=StringIO())
        self.assertEqual(Service.objects.count(), 12)
        service = Service.objects.get(slug='location-espaces')
        service.title = 'Notre salle'
        service.save()
        call_command('seed_showcase', stdout=StringIO())
        service.refresh_from_db()
        self.assertEqual(service.title, 'Notre salle')
        self.assertEqual(Service.objects.count(), 12)

    def test_all_public_pages_render_without_account(self):
        for name in ['home', 'services', 'trainings', 'solutions', 'portfolio', 'about', 'contact', 'faq', 'legal', 'opportunities']:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Demander un devis')
        self.assertEqual(self.client.get(reverse('service_group', args=['location-services-operationnels'])).status_code, 200)
        self.assertEqual(self.client.get(reverse('service_group', args=['inconnu'])).status_code, 404)

    def test_portfolio_only_shows_authorized_entries(self):
        ShowcaseEntry.objects.create(kind='project', title='Projet public', description='Référence autorisée', published=True)
        ShowcaseEntry.objects.create(kind='project', title='Projet secret', description='Confidentiel')
        response = self.client.get(reverse('portfolio'))
        self.assertContains(response, 'Projet public')
        self.assertNotContains(response, 'Projet secret')

    def test_contact_consent_and_rate_limit(self):
        data = {'name': 'Client', 'email': 'client@example.com', 'subject': 'Mon projet', 'message': 'Un besoin de site web'}
        self.assertEqual(self.client.post(reverse('contact'), data).status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())
        data['consent'] = 'on'
        self.assertRedirects(self.client.post(reverse('contact'), data), reverse('contact'))
        self.client.post(reverse('contact'), data)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_honeypot(self):
        response = self.client.post(reverse('contact'), {'name': 'Robot', 'email': 'robot@example.com', 'subject': 'Spam', 'message': 'Spam', 'consent': 'on', 'website': 'spam'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())

    def test_training_calendar_excludes_old_and_unpublished_sessions(self):
        data = dict(description='Programme', audience='Tous', format='Présentiel', duration='2 jours')
        TrainingSession.objects.create(title='Prochaine session', date=timezone.localdate()+timedelta(days=5), published=True, **data)
        TrainingSession.objects.create(title='Ancienne session', date=timezone.localdate()-timedelta(days=5), published=True, **data)
        TrainingSession.objects.create(title='Session confidentielle', **data)
        response = self.client.get(reverse('trainings'))
        self.assertContains(response, 'Prochaine session')
        self.assertNotContains(response, 'Ancienne session')
        self.assertNotContains(response, 'Session confidentielle')
