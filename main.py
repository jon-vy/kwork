import re
import time
from time import sleep

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def get_update():
   t = str(time.time()).split('.')[0]
   URL = 'https://kwork.ru/projects'
   PARAMS = {'c': '41', 'attr': '211'}
   HEADERS = {
      "user-agent": generate_user_agent(),
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      # "Cookie": "__ddg1=EjmK7NRSJ6WeYCMi4PWy; _kmid=fa7954af0b193787252698994fc8d878; _kmfvt=1647194261; site_version=desktop; RORSSQIHEK=8b9de81cd97f602bb52e8580857e33e8; _gcl_au=1.1.63841012.1647194262; _ym_uid=1647194263731052968; _ym_d=1647194263; yandex_client_id=1647194263731052968; _ga=GA1.2.156726322.1647194263; _gid=GA1.2.70225478.1647194263; google_client_id=156726322.1647194263; _ubtcuid=cl0pkxnsv000026daxzbynki5; _sp_ses.b695=*; _sp_id.b695=f6588b35-1bb6-479a-bfca-3b3e40e1c39b.1647194263.1.1647194263.1647194263.b9dc0270-2e0a-46e8-a591-e5539443efd7; _ym_isad=2"

              }
   cookies = dict(cookies_are=f"__ddg1=FdVz6Yd9GTzAFjh4pCUU; _kmid=b66e36ebd3b39e00f5900bc497816831; _kmfvt=1647198552; site_version=desktop; RORSSQIHEK=308573fbbbdf0bf2615e207b2bc5f268; _gcl_au=1.1.1577679482.1647198552; _ym_uid=1647198553503256183; _ym_d=1647198553; yandex_client_id=1647198553503256183; _ubtcuid=cl0pnmsj7000026d7vunibkkr; _sp_ses.b695=*; _sp_id.b695=c327d9b9-9657-4c58-baee-de0feb68c015.1647198554.1.{str(time.time()).split('.')[0]}.1647198554.dddc7757-ac48-4266-9f5a-3e12c1626d7f; _ym_hostIndex=0-2%2C1-0; _ym_isad=2")
   r = requests.get(URL, params=PARAMS, headers=HEADERS, cookies=cookies)
   for key, value in r.request.headers.items():
       print(key + ": " + value)
   print(r.status_code)
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
