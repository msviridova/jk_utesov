from django.contrib import admin
from .models import Apartment, Resident
from passes.models import PassPeople, PassCars


class PassPeopleInLine(admin.TabularInline):
    model = PassPeople
    extra = 0
    readonly_fields = ['name_of_guest', 'created_at', ]

class PassCarsInLine(admin.TabularInline):
    model = PassCars
    extra = 0
    readonly_fields = ['model_car', 'number_car', 'created_at']


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('number',)
    list_display_links = ('number',)
    search_fields = ('number',)
    inlines = [
        PassPeopleInLine,
        PassCarsInLine
    ]


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'contact', 'number_apartment')
    list_display_links = ('name', 'surname', 'contact', 'number_apartment')
    search_fields = ('number_apartment','surname')
    list_filter = ('number_apartment',)


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Resident, ResidentAdmin)
