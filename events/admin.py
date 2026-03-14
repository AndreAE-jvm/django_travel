from django.contrib import admin
from events.models import Event, EventCategory, EventImage, EventRegistration


admin.site.register(EventCategory)
admin.site.register(EventImage)
admin.site.register(EventRegistration)



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_participants', 'category']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['-price']
    fields = ('name', ('price', 'max_participants', 'category'), 'description', 'short_description',
              'location', 'start_datetime', 'end_datetime', 'image')
    readonly_fields = []