from django.db import models
from users.models import User

# Create your models here.
class EventCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='events/')
    description = models.TextField(blank=True)
    short_description = models.TextField(max_length=64,blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_participants = models.PositiveIntegerField(default=15) # В админке поле автоматически заполнится числом 15, если поле пустое
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT) #CASCADE = Удалил категорию → удалились ВСЕ её события;
    # PROTECT = Не даст удалить категорию, пока есть её события #
    location = models.CharField(max_length=200, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    @property
    def duration(self):
        if self.start_datetime and self.end_datetime:
            duration = self.end_datetime - self.start_datetime

            # Получаем дни, часы и минуты
            days = duration.days
            total_hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            # Форматируем вывод
            parts = []
            if days > 0:
                if days == 1:
                    parts.append(f"{days} день")
                elif days in [2, 3, 4]:
                    parts.append(f"{days} дня")
                else:
                    parts.append(f"{days} дней")

            if total_hours > 0:
                parts.append(f"{total_hours} ч")

            if minutes > 0:
                parts.append(f"{minutes} мин")

            if parts:
                return " ".join(parts)
            else:
                return "Менее минуты"

        return "Не указано"

    def __str__(self):
        return f'{self.name} | {self.category.name}'


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Изображение для {self.event.name}"

    class Meta:
        verbose_name = 'Изображение экскурсии'
        verbose_name_plural = 'Изображения экскурсий'


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    tickets_quantity = models.PositiveIntegerField(default=1, verbose_name='Количество билетов')
    registration_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    event_date = models.DateField(verbose_name='Дата события')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    notes = models.TextField(blank=True, null=True, verbose_name='Особые пожелания')

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.event.price * self.tickets_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Регистрация {self.event.name} для {self.user.username}"

    class Meta:
        verbose_name = 'Регистрация на событие'
        verbose_name_plural = 'Регистрации на события'
        ordering = ['-registration_timestamp']







