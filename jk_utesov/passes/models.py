from django.db import models
from apartments.models import Apartment


class PassPeople(models.Model):
    number_apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT, verbose_name='Номер квартиры')
    name_of_guest = models.CharField(max_length=150, verbose_name='Имя гостя',
                                     help_text='Если вы ожидаете курьера, введите "Курьер"')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления заявки')

    def __str__(self):
        return f"Заявка №{self.id} Квартира №{self.number_apartment} Имя гостя {self.name_of_guest}"

    class Meta:
        verbose_name = 'Пропуск для гостя'
        verbose_name_plural = 'Пропуска для гостей'


class PassCars(models.Model):
    number_apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT, verbose_name='Номер квартиры')
    model_car = models.CharField(max_length=150, verbose_name='Марка автомобиля')
    number_car = models.IntegerField(verbose_name='Номер автомобиля')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления заявки')

    def __str__(self):
        return f"Заявка №{self.id} Квартира №{self.number_apartment} Модель автомобиля {self.model_car} " \
               f"Номер автомобиля {self.number_car}"

    class Meta:
        verbose_name = 'Пропуск на авто'
        verbose_name_plural = 'Пропуска на авто'
