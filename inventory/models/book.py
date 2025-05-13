from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    STATUS_CHOICES = [
        ('read', 'Прочитано'),
        ('reading', 'Читается'),
        ('borrowed', 'Одолжено'),
    ]
    GENRE_CHOICES = [
        ('classic', 'Классика'),
        ('fantasy', 'Фэнтези'),
        ('novel', 'Романы'),
        ('horror', 'Ужасы'),
        ('adventure', 'Приключения'),
        ('humor', 'Юмор'),
        ('biography', 'Биографии'),
        ('history', 'История'),
        ('science', 'Наука/Техника'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reading')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='novel')
    ISBN = models.CharField(max_length=20, blank=True, default='')
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']