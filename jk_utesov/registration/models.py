from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from apartments.models import Apartment



class ResidentRequest(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия пользователя')
    number_apartment = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)],
                                           verbose_name='Номер квартиры')
    contact = models.CharField(max_length=150, verbose_name='Контактный номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления заявки')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата рассмотрения')
    chat_id = models.IntegerField(blank=True, verbose_name='Идентификатор пользователя')
    is_accepted = models.BooleanField(default=False, verbose_name='Заявка принята')

    def __str__(self):
        return f"Заявка №{self.id} Квартира №{self.number_apartment} Фамилия {self.surname}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
