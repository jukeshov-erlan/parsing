import requests
from bs4 import BeautifulSoup
import csv


def write_to_csv(data: dict):
    with open('data.csv', 'a') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow((data['title'], data['price'], data['img'], data['description']))


def get_html(urls):
    response = requests.get(urls)
    return response.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find('div', class_='catalog-list').find_all('a')
    for car in cars:
        try:
            title = car.find('span', class_="catalog-item-caption").text.strip()
        except:
            title = ''

        try:
            price = car.find('span', class_='catalog-item-price').text
        except:
            price = ''

        try:
            description = car.find('span', class_='catalog-item-descr').text.replace('\n', '').split()
            description = ''.join(description)
        except:
            description = ''

        try:
            img = car.find('img').get('src')
        except:
            img = ''
            
        data = {
            'title': title,
            'price': price,
            'description': description,
            'img': img
        }
        write_to_csv(data)


def main():
    url = 'https://cars.kg/offers/'
    pages = 105

    with open('data.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['title', 'price', 'img', 'description'])

    for page in range(1, pages + 1):
        urls = url+str(page)
        html = get_html(urls)
        get_data(html)


main()