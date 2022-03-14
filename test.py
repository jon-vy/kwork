import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
from user_agent import generate_user_agent, generate_navigator

def get_ip():
    # HEADERS = {'User-Agent': ua.chrome}
    HEADERS = {'User-Agent': generate_user_agent()}
    URL = 'https://2ip.ru/'
    r = requests.get(URL, headers=HEADERS)
    src = r.content
    # print(src)
    soup = BeautifulSoup(src, "lxml")
    try:
        ip = soup.find('div', id='d_clip_button').text.split()
    except:
        # print('не получил ip')
        ip = soup.find('big', id='d_clip_button').text.split()
    print(ip)
    # какие заголовки я отправляю
    for key, value in r.request.headers.items():
        print(key + ": " + value)

if __name__ == '__main__':
    get_ip()