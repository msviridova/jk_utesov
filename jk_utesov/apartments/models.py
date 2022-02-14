from django.db import models


class Apartment(models.Model):
    number = models.IntegerField(primary_key=True, verbose_name='Номер квартиры')

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'


class Resident(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Имя жителя')
    surname = models.CharField(max_length=150, db_index=True, verbose_name='Фамилия жителя')
    contact = models.CharField(max_length=50, verbose_name='Номер телефона')
    number_apartment = models.ForeignKey('Apartment', on_delete=models.PROTECT, verbose_name='Номер квартиры')
    chat_id = models.IntegerField(blank=True, verbose_name='Идентификатор пользователя')

    def __str__(self):
        return self.name + ' ' + self.surname

    class Meta:
        verbose_name = 'Житель квартиры'
        verbose_name_plural = 'Жители квартиры'
