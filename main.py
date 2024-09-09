import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://news.tyuiu.ru/sections/arxid?page='

def get_news_from_page(page_number):
    url = f"{base_url}{page_number}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_container = soup.find('div', class_='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-9 mb-6')
        if news_container is None:
            return []

        news_items = news_container.find_all('a', class_='space-y-5 group-link-underline')

        news_list = []

        for item in news_items:
            title_tag = item.find('span', class_='title !text-base lg:!text-lg font-medium')
            title = title_tag.get_text(strip=True) if title_tag else ''

            image_tag = item.find('img')
            image = image_tag['src'] if image_tag else ''

            date_tag = item.find('div', class_='flex flex-wrap gap-2 justify-between mb-2 text-gray-400 font-medium text-sm').find_all('p')[1]
            date = date_tag.get_text(strip=True) if date_tag else ''

            link = item['href'] if item else ''
            summary = get_summary_from_link(link)

            news_data = {
                "title": title,
                "summary": summary,
                "image": image,
                "date": date,
                "link": link,
                "view_count": 0,
                "like_count": 0,
                "dislike_count": 0
            }

            news_list.append(news_data)
        return news_list
    else:
        return []

def get_summary_from_link(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_container = soup.find('div', class_='paragraph-text', itemprop='null')
        if text_container:
            full_text = text_container.get_text(strip=True)
            return full_text
    return ''

all_news = []
page_number = 1

while True:
    news_from_page = get_news_from_page(page_number)
    if not news_from_page:
        break
    all_news.extend(news_from_page)
    page_number += 1

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(all_news, f, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в news.json")
