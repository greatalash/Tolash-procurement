from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'company.html')

def pricing(request):
    return render(request, 'pricing.html')


def home(request):
    product = None
    if request.method == 'POST':
        link = request.POST.get('link')
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            title = soup.title.string.strip()
            image = soup.find('img')
            price = 20  # Placeholder price since 1688 uses dynamic JS (need Selenium for real)
            exchange_rate = 120  # Set manually or from API
            naira_price = price * exchange_rate

            product = {
                'title': title,
                'image': image['src'] if image else '',
                'price': price,
                'naira_price': naira_price
            }
        except Exception as e:
            product = {'title': 'Error fetching product', 'price': 0, 'naira_price': 0, 'image': ''}

    return render(request, 'home.html', {'product': product})
