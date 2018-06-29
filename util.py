from bs4 import BeautifulSoup
import requests

def get(url):
    print('getting %s' % url)
    try:
        r = requests.get(url)
    except Error as e:
        print('uh oh')
        print(e)

def fakeEngagement(html):
    soup = BeautifulSoup(html)

    links = soup.findAll('a')
    get(links[0].get('href'))
    imgs = soup.findAll('img')
    get(imgs[-1].get('src'))

