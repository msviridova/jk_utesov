from django.contrib import admin
from .models import *


class PassPeopleAdmin(admin.ModelAdmin):
    list_display = ('number_apartment', 'name_of_guest', 'created_at')
    list_display_links = ('number_apartment', 'name_of_guest', 'created_at')
    search_fields = ('number_apartment', 'name_of_guest', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ['number_apartment', 'name_of_guest', 'created_at']


class PassCarsAdmin(admin.ModelAdmin):
    list_display = ('number_apartment', 'model_car', 'number_car','created_at')
    list_display_links = ('number_apartment', 'model_car', 'number_car','created_at')
    search_fields = ('number_apartment', 'model_car', 'number_car','created_at')
    list_filter = ('created_at',)
    readonly_fields = ['number_apartment', 'model_car', 'number_car','created_at']


admin.site.register(PassPeople, PassPeopleAdmin)
admin.site.register(PassCars, PassCarsAdmin)
