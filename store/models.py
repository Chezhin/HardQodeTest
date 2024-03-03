from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    """
    Модель продукта.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='products_created'
    )
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_start = models.DateTimeField('Дата начала занятий')
    min_users = models.PositiveIntegerField(default=0)
    max_users = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    """
    Модель Урока.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    video_link = models.URLField()

    def __str__(self):
        return self.title
    

class Group(models.Model):
    """
    Модель группы.
    """
    title = models.CharField(max_length=200)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    students = models.ManyToManyField(User, related_name='group_students')

    def __str__(self):
        return f"{self.title} | Количество студентов {self.students.count()}"
