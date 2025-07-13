from django.contrib import admin 
from inventory.models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'user')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'author', 'ISBN')

admin.site.register(Book, BookAdmin)  # Явная регистрация