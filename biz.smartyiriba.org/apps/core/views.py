from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.forms import RegistrationForm
from apps.catalog.models import Service
from apps.quotes.forms import QuoteRequestForm
from apps.quotes.models import QuoteRequest
from django.conf import settings
from django.core.cache import cache
from .models import ShowcaseEntry, TrainingSession
from .forms import ContactForm
from .showcase import SERVICE_GROUPS, TRAINING_TOPICS, FAQ, COMPETENCIES

def home(request):
    return render(request, 'home.html', {'services': Service.objects.filter(active=True).select_related('category')[:6], 'groups': SERVICE_GROUPS, 'projects': ShowcaseEntry.objects.filter(kind='project', published=True)[:3]})
def services(request):
    return render(request, 'services.html', {'services': Service.objects.filter(active=True).select_related('category'), 'groups': SERVICE_GROUPS})
def service_detail(request, slug):
    return render(request, 'service.html', {'service': get_object_or_404(Service, slug=slug, active=True)})
def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Créer mon compte', 'button': 'Créer mon compte'})
def quote(request):
    form = QuoteRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        if request.user.is_authenticated:
            item.customer = request.user
        item.save()
        messages.success(request, 'Votre demande a été enregistrée. Référence : ' + str(item.reference))
        return redirect('quote_success')
    if request.method != 'POST':
        service = Service.objects.filter(active=True, slug=request.GET.get('service', '')).first()
        if service:
            form.fields['service'].initial = service.pk
    return render(request, 'form.html', {'form': form, 'title': 'Demander un devis', 'button': 'Envoyer ma demande'})
def quote_success(request):
    return render(request, 'quote_success.html')
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'quotes': QuoteRequest.objects.filter(customer=request.user)})

def service_group(request, slug):
    from django.http import Http404
    group = next((group for group in SERVICE_GROUPS if group['slug'] == slug), None)
    if group is None:
        raise Http404
    return render(request, 'showcase/group.html', {'group': group, 'services': Service.objects.filter(active=True, category__slug=slug)})

def trainings(request):
    from django.utils import timezone
    from django.db.models import Q
    sessions = TrainingSession.objects.filter(published=True).filter(Q(date__isnull=True) | Q(date__gte=timezone.localdate()))
    return render(request, 'showcase/trainings.html', {'topics': TRAINING_TOPICS, 'sessions': sessions, 'programs': sessions.filter(program=True)})

def solutions(request):
    return render(request, 'showcase/solutions.html')

def about(request):
    return render(request, 'showcase/about.html', {'team': ShowcaseEntry.objects.filter(kind='team', published=True), 'competencies': COMPETENCIES})

def portfolio(request):
    return render(request, 'showcase/portfolio.html', {'projects': ShowcaseEntry.objects.filter(kind='project', published=True), 'clients': ShowcaseEntry.objects.filter(kind='client', published=True)})

def faq(request):
    return render(request, 'showcase/faq.html', {'questions': FAQ})

def opportunities(request):
    return render(request, 'showcase/entries.html', {'title': 'Opportunités commerciales', 'intro': 'Consultants, formateurs, fournisseurs et prestataires : retrouvez ici les besoins de collaboration publiés par Smart YIRIBA.', 'entries': ShowcaseEntry.objects.filter(kind='opportunity', published=True)})

def legal(request):
    return render(request, 'showcase/entries.html', {'title': 'Documents légaux et commerciaux', 'intro': 'Les conditions applicables à chaque prestation sont précisées avant engagement. Contactez-nous pour obtenir les documents relatifs à votre demande.', 'entries': ShowcaseEntry.objects.filter(kind='legal', published=True)})

def contact(request):
    initial = {'subject': request.GET.get('objet', '')[:200]}
    form = ContactForm(request.POST if request.method == 'POST' else None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        # Cache local en développement ; cache partagé requis avec plusieurs workers.
        import hashlib
        key = 'contact:' + hashlib.sha256(request.META.get('REMOTE_ADDR', '').encode()).hexdigest()
        if not cache.add(key, True, 60):
            form.add_error(None, 'Veuillez patienter une minute avant une nouvelle demande.')
        else:
            form.save()
            messages.success(request, 'Votre message a été enregistré. Notre équipe vous recontactera pour répondre à votre demande.')
            return redirect('contact')
    return render(request, 'showcase/contact.html', {'form': form, 'contact': settings.BUSINESS_CONTACT})
