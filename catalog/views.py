from django.db.models import Count
from django.shortcuts import render

from bot.books_data import BOOKS_CATALOG
from .models import UserQuery


def _topics():
    return [
        {'key': k, 'title': k.capitalize(), 'count': len(v)}
        for k, v in BOOKS_CATALOG.items()
    ]


def index(request):
    return render(request, 'catalog/index.html', {'topics': _topics()})


def books(request):
    selected = request.GET.get('topic', '').strip().lower()
    if selected not in BOOKS_CATALOG:
        selected = ''

    items = [(selected, BOOKS_CATALOG[selected])] if selected else BOOKS_CATALOG.items()
    sections = [
        {'key': k, 'title': k.capitalize(), 'books': books_list}
        for k, books_list in items
    ]

    return render(request, 'catalog/books.html', {
        'topics':   _topics(),
        'sections': sections,
        'selected': selected,
    })


def dashboard(request):
    by_status = dict(UserQuery.objects.values_list('status').annotate(n=Count('id')))
    return render(request, 'catalog/dashboard.html', {
        'queries':      UserQuery.objects.all()[:50],
        'total':        UserQuery.objects.count(),
        'unique_users': UserQuery.objects.values('telegram_id').distinct().count(),
        'answered':     by_status.get('answered', 0),
        'pending':      by_status.get('pending', 0),
        'support':      by_status.get('support', 0),
    })
