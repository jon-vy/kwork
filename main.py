import re
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import html

from fake_useragent import UserAgent
ua = UserAgent()


def get_update():
   URL = 'https://kwork.ru/projects'
   PARAMS = {'c': '41', 'attr': '211'}
   HEADERS = {'user-agent': ua.chrome}
   r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
   # for key, value in r.request.headers.items():
   #     print(key + ": " + value)
   # print(r.status_code)
   if r.status_code == 200:
      src = r.content
   else:
      return r.status_code

   # print(src)

   # f = open('data/index.html', 'w', encoding='utf-8')
   # f.write(r.text)

   # with open('data/index.html', 'r', encoding='utf-8') as f:
   #    src = f.read()

   soup = BeautifulSoup(src, "lxml")
   divs = soup.findAll("div", class_=re.compile("card__content"))
   # print(divs[0])
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

   return r.status_code


if __name__ == '__main__':
   while True:
      st_code = get_update()
      if st_code == 200:
         sleep(5)
      else:
         requests.get('https://api.telegram.org/bot1548910949:AAG0L82sa5NpBW9sMxUIFOtw8cc4ONdCimA/sendMessage',
                      params={
                         'chat_id': '791687256',
                         'text': f"Бот остановлен status_code {st_code}"
                      }
                      )
         break
