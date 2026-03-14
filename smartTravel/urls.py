
"""
URL configuration for smartTravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from events.views import index, events
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import Http404

# # Кастомный обработчик 404
# def custom_page_not_found(request, exception):
#     return render(request, 'events/404.html', status=404)
#
# # Функция для тестирования 404
# def test_404(request):
#     raise Http404("Тестовая 404 страница")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('events/', include('events.urls', namespace='events')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/login/', RedirectView.as_view(url='/users/login/', permanent=False)),
    path('terms/', TemplateView.as_view(template_name='events/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='events/privacy.html'), name='privacy'),
    path('refund/', TemplateView.as_view(template_name='events/refund.html'), name='refund'),

    # ТЕСТОВЫЙ URL ДЛЯ 404
    # path('test404/', test_404),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# принудительно раздаем медиа даже при DEBUG=False
# if not settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#
# handler404 = custom_page_not_found
