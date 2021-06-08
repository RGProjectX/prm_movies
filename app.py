from typing import Optional
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
import lxml
def main(category,page):
    url = f'https://prmovies.mx/genre/{category}/page/{page}/'
    req = requests.get(url)
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text,'lxml')
            data = {
            "website_url": url,
            "category": category,
            "results" : [{
                'title': x.a.get('oldtitle'),
                "lang": x.span.text,
                "thumbnail": x.img.get('data-original'),
                "slug" : x.a.get('href').replace('https://prmovies.mx/','')} for x in soup.find_all('div',class_='ml-item')]}
            return data
        except Exception as e:
            return {
                "error":e,
                "website_url": url,
                "category": category,
            }

def details(slug):
    slug_url=f'https://prmovies.mx/{slug}'
    req = requests.get(slug_url)
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text,'lxml')
            data = {
                'title': soup.find('h3',attrs={'itemprop':'name'}).text,
                'duration': soup.find('span',attrs={'itemprop':'duration'}).text,
                'desc': soup.find('p',class_='f-desc').text,
                'genre': ','.join([x.text for x in soup.find('div',class_='mvici-left').find_all('a',attrs={'rel':'category tag'})]),
                'link': if soup.find('a',class_='lnk-lnk lnk-1').get('href') is None: soup.find('iframe').get('src')
            }
            return data
        except Exception as e:
             return {
                "error":e,
                "website_url": slug_url,
                "slug": slug,
            }

app =  FastAPI()

@app.get("/content/")
def get_content(category: str, page: Optional[str] = 1,slug: Optional[str] = None):
    if slug == None:
        return main(category,page)
    return details(slug)
