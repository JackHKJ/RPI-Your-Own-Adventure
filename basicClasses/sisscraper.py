import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from dotenv import load_dotenv
import re
import time

transcript_url = 'https://sis.rpi.edu/rss/bwskotrn.P_ViewTran'

class SISscraper:

    def __init__(self, rin, password):
        self.__LOGIN_BASE_PARAMS = f"username={rin}&password={urllib.parse.quote(password)}&_eventId=submit"
        self.__LOGIN_RETRY_NUM = 3
        self.__session = requests.Session()

    @property
    def logged_in(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        login_url = "https://cas-auth-ent.rpi.edu/cas/login?service=https%3A%2F%2Fbannerapp04-bnrprd.server.rpi.edu%3A443%2Fssomanager%2Fc%2FSSB"
        login_page = self.__session.get(url=login_url)
        login_soup = BeautifulSoup(login_page.text.encode("utf8"), "html.parser")
        csrf = login_soup.find("input", attrs={"name": "execution"})["value"]
        login_params = self.__LOGIN_BASE_PARAMS + f"&execution={csrf}"

        response = self.__session.request(
            "POST",
            login_url,
            headers=headers,
            data=login_params,
        )

        text = response.text.encode("utf8")
        if b"Main Menu" not in text:
            return False
        return True

    def get_learned_courses(self):
        response = self.__session.request('POST', transcript_url, data=f"levl=&tprt=UWEB")  
        transcript_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')
        course_dept = transcript_soup.find_all('td', class_='dddefault', string=re.compile('^[A-Z]{4}$'))
        course_num = transcript_soup.find_all('td', class_='dddefault', string=re.compile('^[0-9]{4}$'))
        return [x.next_element + '-' + y.next_element for x, y in zip(course_dept, course_num)]

if __name__ == '__main__':
    load_dotenv()
    scraper = SISscraper(os.getenv('RIN'), os.getenv('PASSWORD'))
    print(scraper.logged_in())
    print(scraper.get_learned_courses())