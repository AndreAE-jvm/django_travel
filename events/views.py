from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from events.models import Event, EventCategory, EventRegistration
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse



def index(request):
    return render(request, 'events/index.html', {'title': 'SmartTravel'})


# константы
events_page = 6
registrations_page = 6

from datetime import datetime


def events(request, category_id=None, page=1):
    # базовый контекст
    context = {
        'title': 'Events | SmartTravel',
        'categories': EventCategory.objects.all(),
        'category_id': category_id,
    }

    # получаем параметры из GET-запроса
    search_query = request.GET.get('search', '')

    # Получаем даты из скрытых полей
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')


    context.update({
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
    })

    # базовый запрос с сортировкой
    filtered_events = Event.objects.all().order_by('id')

    # фильтр по категории
    if category_id:
        filtered_events = filtered_events.filter(category_id=category_id)

    # ПОИСК ПО ТЕКСТУ (регистронезависимый)
    if search_query:
        filtered_events = filtered_events.filter(
            Q(name__icontains=search_query) |
            Q(name__icontains=search_query.lower()) |
            Q(name__icontains=search_query.upper()) |
            Q(name__icontains=search_query.capitalize())
        ).distinct()

    # ФИЛЬТР ПО ДАТАМ
    if date_from:
        filtered_events = filtered_events.filter(start_datetime__date__gte=date_from)

    if date_to:
        filtered_events = filtered_events.filter(start_datetime__date__lte=date_to)

    # аннотируем длительность
    filtered_events = filtered_events.annotate(
        duration_calc=F('end_datetime') - F('start_datetime')
    )

    # пагинация
    paginator = Paginator(filtered_events, events_page)
    events_paginator = paginator.get_page(page)

    context['events'] = events_paginator
    return render(request, "events/events.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Свободные места
    registered = EventRegistration.objects.filter(
        event=event, event_date=event.start_datetime.date(),
        status__in=['pending', 'confirmed']
    ).aggregate(total=Sum('tickets_quantity'))['total'] or 0

    event.available_spots = event.max_participants - registered

    return render(request, 'events/event_detail.html', {
        'event': event,
        'images': event.images.all(),
    })


@login_required
def create_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('events:detail', args=[event_id]))

    tickets_quantity = int(request.POST.get('tickets_quantity', 1))

    registered = EventRegistration.objects.filter(
        event=event,
        event_date=request.POST.get('event_date'),
        status__in=['pending', 'confirmed']
    ).aggregate(total=Sum('tickets_quantity'))['total'] or 0

    available_spots = event.max_participants - registered

    if tickets_quantity > available_spots:
        messages.warning(request, f'Доступно только {available_spots} мест')
        return HttpResponseRedirect(reverse('events:detail', args=[event_id]))

    registration = EventRegistration.objects.create(
        user=request.user,
        event=event,
        tickets_quantity=tickets_quantity,
        event_date=request.POST.get('event_date'),
        total_price=event.price * tickets_quantity,
        notes=request.POST.get('notes', ''),
        status='pending'
    )

    messages.success(request, 'Бронирование создано! Статус: ожидает подтверждения')
    return HttpResponseRedirect(reverse('events:registration_detail', args=[registration.id]))


@login_required
def my_registrations(request):
    status_filter = request.GET.get('status', 'all')
    page = request.GET.get('page', 1)

    registrations = EventRegistration.objects.filter(user=request.user)
    if status_filter != 'all':
        registrations = registrations.filter(status=status_filter)
    registrations = registrations.order_by('-registration_timestamp')

    paginator = Paginator(registrations, registrations_page)

    try:
        registrations_paginator = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):

        registrations_paginator = paginator.page(1)
    context = {
        'title': 'Мои бронирования',
        'registrations': registrations_paginator,
        'current_status': status_filter,

    }
    return render(request, 'events/my_registrations.html', context)


@login_required
def registration_detail(request, registration_id):
    registration = get_object_or_404(EventRegistration, id=registration_id, user=request.user)
    return render(request, 'events/registration_detail.html', {

        # Реализация сортировки, фильтрации и бронирования экскурсий
        'title': f'Бронирование {registration.event.name}',
        'registration': registration,
    })


@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(EventRegistration, id=registration_id, user=request.user)

    if registration.status in ['pending', 'confirmed']:
        EventRegistration.objects.filter(id=registration_id).update(status='cancelled')

    return HttpResponseRedirect(reverse('events:my_registrations'))
