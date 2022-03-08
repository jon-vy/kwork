import re
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import html

def get_update():
   URL = 'https://kwork.ru/projects'
   PARAMS = {'c': '41', 'attr': '211'}
   HEADERS = {'authority': 'kwork.ru',
              'method': 'GET',
              'path': '/projects?c=41&attr=211',
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'ru,en;q=0.9',
              'cache-control': 'max-age=0',
              'cookie': '__ddg1=poL9UjWWXrOyP2iyP9vy; _kmid=36dae6a50856a67d73d34f775278352f; _kmfvt=1646764185; site_version=desktop; RORSSQIHEK=1361df32a0e26f803b5df379735ad865',
              'sec-ch-ua': '" Not;A Brand";v="99", "Yandex";v="91", "Chromium";v="91"',
              'sec-ch-ua-mobile': '?0',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'none',
              'sec-fetch-user': '?1',
              'upgrade-insecure-requests': '1',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
              }
   r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
   for key, value in r.request.headers.items():
       print(key + ": " + value)
   print(r.status_code)
   if r.status_code == 200:
      src = r.content
   else:
      print(r.status_code)

   # print(src)

   # f = open('data/index.html', 'w', encoding='utf-8')
   # f.write(r.text)

   # with open('data/index.html', 'r', encoding='utf-8') as f:
   #    src = f.read()

   soup = BeautifulSoup(src, "lxml")
   divs = soup.findAll("div", class_=re.compile("card__content"))
   print(divs[0])
   file_id = open('id.txt', 'r+', encoding='utf-8')
   id_s = file_id.read()
   # print(id_s)
   for div in divs:
      url = div.find('a').get('href')
      id = url.split('/')[-1]
      # print(f"проверка {id}")
      c = id_s.count(id)
      # print(c)
      if c > 0:
         print(f'{id} id существует')
         break
      else:
         print(f'{id} id не существует')
         file_id.write(id + '\n')
         title = div.find('a').text
         descr = div.find("div", class_=re.compile("breakwords")).nextSibling.text
         price = div.find("div", class_=re.compile("wants-card__header-price")).text
         how_much = div.find("div", class_=re.compile("force-font")).text
         requests.get('https://api.telegram.org/bot1548910949:AAG0L82sa5NpBW9sMxUIFOtw8cc4ONdCimA/sendMessage',
                      params={
                         'chat_id': '791687256',
                         'text': f"{title}'\n------------------------------------\n'{price}'\n------------------------------------\n'{descr}'\n------------------------------------\n'{how_much}'\n------------------------------------\n'{url}"
                      }
                      )
         # print(title + ' ' + how_much)
         # print(url_txt +' '+ url +' '+ id)

   # print(divs[0])
   file_id.close()


if __name__ == '__main__':
   while True:
      get_update()
      sleep(5)
