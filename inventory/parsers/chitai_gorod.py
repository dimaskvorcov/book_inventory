# inventory/parsers/chitai_gorod.py
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from django.conf import settings  # Добавляем Django-зависимость

# Используем MEDIA_ROOT Django для хранения обложек
COVERS_DIR = os.path.join(settings.MEDIA_ROOT, "book_covers")
os.makedirs(COVERS_DIR, exist_ok=True)

def fetch_book_html_by_isbn(isbn):
    """Получаем HTML страницу с результатами поиска по ISBN"""
    url = f"https://www.chitai-gorod.ru/search?phrase={isbn}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None

def parse_book_data_from_html(html, isbn):
    """Парсим данные о книге из HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    products_list = soup.find('div', class_='app-products-list')
    if not products_list:
        return None
        
    book_card = products_list.find('article', class_='product-card')
    if not book_card:
        return None
    
    title = book_card.find('a', class_='product-card__title').get('title', '').split('(')[0].strip()
    author = book_card.find('span', class_='product-card__subtitle').get('title', '').strip()
    genre = book_card.get('data-chg-product-category-title', '')
    
    img_tag = book_card.find('img', class_='product-card__image')
    image_path = ''
    
    if img_tag:
        srcset = img_tag.get('srcset', '')
        if srcset:
            variants = [v.strip() for v in srcset.split(',')]
            for variant in variants:
                if '2x' in variant:
                    image_path = variant.split(' ')[0]
                    break
            if not image_path and variants:
                image_path = variants[0].split(' ')[0]
        if not image_path:
            image_path = img_tag.get('src', '')
    
    return {
        'title': title,
        'author': author,
        'genre': genre,
        'image_path': image_path,
        'isbn': isbn,
        'url': urljoin('https://www.chitai-gorod.ru/', book_card.find('a', class_='product-card__title').get('href', ''))
    }

def download_cover(image_url, isbn):
    """Загружает обложку книги"""
    if not image_url:
        return None
    
    clean_url = image_url.split('?')[0] if '?' in image_url else image_url
    filename = f"{isbn}.jpg"
    save_path = os.path.join(COVERS_DIR, filename)
    
    try:
        response = requests.get(clean_url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        
        return f"book_covers/{filename}"  # Возвращаем относительный путь для Django
    except Exception as e:
        print(f"Ошибка при загрузке обложки: {e}")
        return None

# Удаляем main(), так как будем использовать через Django