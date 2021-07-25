import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# Create your views here.

BASE_CRAIGSLIST_URL = 'https://newyork.craigslist.org/d/for-sale/search/sss?query={}'
# https://newyork.craigslist.org/d/for-sale/search/sss?query=car&sort=rel

def home(request) :
    return render(request,'cclone/base.html')

def new_search(request) :
    your_search = request.POST.get('search')
    models.Search.objects.create(search_field = your_search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(your_search))
    print(final_url)

    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features = 'html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings :
        post_title = post.find(class_= 'result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_= 'result-price') :
            post_price = post.find(class_= 'result-price').text
        else :
            post_price = 'N/A'

        if post.find('img') :
            post_img = post.find('img')['src']
        else :
            post_img = f'https://craigslist.org/images/peace.jpg'


        final_postings.append((post_title, post_url, post_price, post_img))


    context = {
        'your_search' : your_search,
        'final_postings' : final_postings,
    }
    return render(request, 'cclone/new_search.html', context)
