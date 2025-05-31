from django.db import models


class Contact(models.Model):
    """Модель Контактов"""
    email = models.EmailField()
    country = models.CharField(
        max_length=100
    )
    city = models.CharField(
        max_length=100
    )
    street = models.CharField(
        max_length=100
    )
    house_number = models.CharField(
        max_length=20
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    """ Модель продукта """
    name = models.CharField(
        max_length=150,
        verbose_name='Наименование',
        unique=True
    )
    model = models.CharField(
        max_length=150,
        verbose_name='Модель',
        unique=True
    )
    release_date = models.DateField(
        verbose_name='Дата выхода продукта на рынок'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Network(models.Model):
    """Модель сети поставщиков"""
    FACTORY = 0
    RETAIL = 1
    ENTREPRENEUR = 2

    LEVEL_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(
        max_length=150,
        verbose_name='Наименование',
        unique=True
    )
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        verbose_name='Уровень поставщика',
        editable=False,
        null=True,
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Контакты'
    )
    products = models.ManyToManyField(
        Product,
        verbose_name='Продукт'
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Поставщик'
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Задолженность перед поставщиком'
    )
    created_at = models.DateField(
        verbose_name='Дата создания', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"

    def _update_level(self):
        """Внутренний метод для обновления уровня"""
        if self.supplier:
            self.level = min(self.supplier.level + 1, self.ENTREPRENEUR)
        else:
            self.level = self.FACTORY

    def save(self, *args, **kwargs):
        """Переопределенный метод сохранения"""
        self._update_level()
        super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     """Автоматически устанавливаем уровень при сохранении"""
    #     if not hasattr(self, 'level') or self.level is None:
    #         if self.supplier:
    #             self.level = min(self.supplier.level + 1, self.ENTREPRENEUR)
    #         else:
    #             self.level = self.FACTORY
    #     super().save(*args, **kwargs)
