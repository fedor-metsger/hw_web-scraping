
import requests
import time
import re
from bs4 import BeautifulSoup
import fake_useragent
from pprint import pprint

PAGE_SIZE = 20

def parse_salary(tag: str) -> (int, int, str):
    tag = re.sub("\s+", "", tag)
    numbers = re.findall("[\d+ ]+", tag)
    fr, to, cur = None, None, "USD" if tag[-3:] == "USD" else "RUR"
    if len(numbers) == 2:
        fr, to = numbers[0], numbers[1]
    elif len(numbers) == 1 and tag[:2] == "от":
        fr = numbers[0]
    elif len(numbers) == 1 and tag[:2] == "до":
        to = numbers[0]
    return fr, to, cur

def scrape_data(kw: str) -> list:
    URL = "https://hh.ru/search/vacancy"
    ua = fake_useragent.UserAgent()
    params = {"page": 0, "text": kw, "items_on_page": PAGE_SIZE, "area": [1, 2]}
    headers = {"user-agent": ua.random}
    res = []
    try:
        result = requests.get(URL, headers=headers, params=params)
        if result.status_code != 200:
            print("Ошибка при запросе данных с сайта HeadHunter: Status code ", response.status_code)
            return None

        soup = BeautifulSoup(result.content, 'html.parser')
        total_pages = None
        # try:
        var = soup.find('div', {"class": "pager"})
        total_pages = int(soup.find(
                                  'div', {"class": "pager"}
                                   ).find_all(
                                   "span", reqursive=False)[-4].find("a").find("span").text)
        # except:
        #     pass
        print(f"Всего найдено {total_pages} страниц")
        for p in range(total_pages):
            time.sleep(1)
            print(f"Загружается страница {p}")
            params = {"page": p, "text": kw, "items_on_page": PAGE_SIZE, "area": [1, 2]}
            headers = {"user-agent": ua.random}
            result = requests.get(f'https://hh.ru/search/vacancy', params=params, headers=headers)
            soup = BeautifulSoup(result.content, 'html.parser')
            links = soup.find_all("div", {"class":"vacancy-serp-item-body__main-info"})
            for v in links:
                salary_from, salary_to, currency =  None, None, None
                name = v.find("a", {"class": "serp-item__title"}).text
                url = v.find("a", {"class": "serp-item__title"}).attrs["href"]
                if v.find("span", {"class": "bloko-header-section-3"}):
                    salary_from, salary_to, currency = parse_salary(v.find("span", {"class": "bloko-header-section-3"}).text)
                company = v.find("div", {"class": "vacancy-serp-item__meta-info-company"}).text
                city = v.find("div", {"class": "vacancy-serp-item__info"}).find_all(
                    "div", {"class": "bloko-text"})[-1].text.split()[0]
#                print(name, url, company, salary_from, salary_to, currency, city)
                res.append({"name": name, "company": company, "url": url, "salary_from": salary_from,
                        "salary_to": salary_to, "currency": currency, "city": city})
            time.sleep(1)
        return res
    except Exception as e:
        print("Ошибка при запросе данных с сайта HeadHunter:", repr(e))
        return None

def main():
    res = scrape_data("Flask Django")
#    pprint(res)

if __name__ == "__main__":
    main()
