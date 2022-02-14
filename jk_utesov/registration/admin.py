from django.contrib import admin
from .models import *
from apartments.models import *


class ResidentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_apartment', 'surname', 'created_at', 'is_accepted')
    list_display_links = ('id', 'number_apartment', 'surname', 'created_at', 'is_accepted')
    search_fields = ('apartment', 'surname')
    list_filter = ('created_at', 'is_accepted')
    actions = ['make_registration']


    def make_registration(self, request, queryset):
        from run_bot import send_message
        for order in queryset:
            register_apartment = Apartment.objects.get_or_create(number=order.number_apartment)
            register_apartment[0].save()

            register_resident = Resident.objects.get_or_create(name=order.name,
                                    surname=order.surname,
                                    contact=order.contact,
                                    number_apartment=Apartment.objects.get(number=order.number_apartment),
                                    chat_id=order.chat_id)
            register_resident[0].save()

            order.is_accepted = True
            order.save()

            send_message(order.chat_id, f'Ваша заявка на регистрацию одобрена.'
                                        f'Теперь вы можете заказывать пропуск через этот бот')


admin.site.register(ResidentRequest, ResidentRequestAdmin)
