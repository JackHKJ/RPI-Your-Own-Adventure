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
        self.LOGIN_BASE_PARAMS = f"username={rin}&password={urllib.parse.quote(password)}&_eventId=submit"
        self.LOGIN_RETRY_NUM = 3

    def __login(self, s):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        login_url = "https://cas-auth-ent.rpi.edu/cas/login?service=https%3A%2F%2Fbannerapp04-bnrprd.server.rpi.edu%3A443%2Fssomanager%2Fc%2FSSB"
        login_page = s.get(url=login_url)
        login_soup = BeautifulSoup(login_page.text.encode("utf8"), "html.parser")
        csrf = login_soup.find("input", attrs={"name": "execution"})["value"]
        login_params = self.LOGIN_BASE_PARAMS + f"&execution={csrf}"

        response = s.request(
            "POST",
            login_url,
            headers=headers,
            data=login_params,
        )

        text = response.text.encode("utf8")
        if b"Main Menu" not in text:
            return False, text
        return True, None

    def get_courses(self):
        with requests.Session() as s:
            for _ in range(self.LOGIN_RETRY_NUM):
                result, data = self.__login(s)
                if result:
                    break
                s.cookies.clear()
                time.sleep(30)
            else:
                print(f"Failed to login to SIS {data}")
                exit(1)

            response = s.request('POST', transcript_url, data=f"levl=&tprt=UWEB")  
            transcript_soup = BeautifulSoup(response.text.encode('utf8'), 'html.parser')
            course_dept = transcript_soup.find_all('td', class_='dddefault', string=re.compile('^[A-Z]{4}$'))
            course_num = transcript_soup.find_all('td', class_='dddefault', string=re.compile('^[0-9]{4}$'))
            return [x.next_element + '-' + y.next_element for x, y in zip(course_dept, course_num)]

if __name__ == '__main__':
    load_dotenv()
    scraper = SISscraper(os.getenv('RIN'), os.getenv('PASSWORD'))
    print(scraper.get_courses())