from django.urls import path
from events.views import events, event_detail, my_registrations, registration_detail, cancel_registration, \
    create_registration

app_name = 'events'

urlpatterns = [
    # Главная страница событий (без категории)
    path('', events, name='index'),  # Это для /events/

    # Страница с категорией
    path('category/<int:category_id>/', events, name='category'),

    # Пагинация
    path('page/<int:page>/', events, name='page'),

    # Детальная страница события
    path('event/<int:event_id>/', event_detail, name='detail'),

    # Регистрация на событие
    path('event/<int:event_id>/register/', create_registration, name='create_registration'),

    # Мои бронирования
    path('my-registrations/', my_registrations, name='my_registrations'),
    path('my-registrations/<str:status>/', my_registrations, name='my_registrations_filtered'),

    # Детали бронирования
    path('registration/<int:registration_id>/', registration_detail, name='registration_detail'),
    path('registration/<int:registration_id>/cancel/', cancel_registration, name='cancel_registration'),

]
