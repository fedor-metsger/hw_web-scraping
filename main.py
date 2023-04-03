
import requests
import json
from pprint import pprint

OUTPUT_FILENAME = "hh.json"
PAGE_SIZE = 100

def request_datapage(pg: int, kw: str) -> (list, int):

    url = "https://api.hh.ru/vacancies"
    params = {
        'host': "hh.ru",
        "text": kw,
        "area": [1, 2],
        "page": pg,
        "per_page": PAGE_SIZE
    }
    res, pages = [], 0
    try:
        response = requests.get(url, params=params)
        pages = response.json()["pages"]
        for i in response.json()["items"]:
            # print(i["id"])
            company, descr, salary_from, salary_to, currency, city = None, None, None, None, None, None
            if isinstance(i["employer"], dict): company = i["employer"]["name"]
            if isinstance(i["snippet"], dict): descr = i["snippet"]["responsibility"]
            if isinstance(i["area"], dict): city = i["area"]["name"]
            if isinstance(i["salary"], dict):
                salary_from = i["salary"]["from"]
                salary_to = i["salary"]["to"]
                currency = i["salary"]["currency"]
            # res.append(HHVacancy(i["name"], i["employer"]["name"], i["url"], i["snippet"]["responsibility"], i["salary"]["from"]))
            res.append({"name": i["name"], "company": company, "url": i["url"], "descr": descr,
                        "salary_from": salary_from, "salary_to": salary_to, "currency": currency,
                        "url": i["url"], "city": city})
    except Exception as e:
        print("Ошибка при запросе данных с сайта HeadHunter:", repr(e))
        return None, None

    return res, pages

def request_data(kw:str) -> list:
    print(f'Выполняется загрузка вакансий с сайта HeadHunter c ключевыми словами "{kw}"')

    data, pg = [], 0
    while True:
        ret_data, ret_pages = request_datapage(pg, kw)
        if ret_data == None or ret_data == []: return ret_data
        if ret_data == []:
            print(f"Нет вакансий с такими ключевыми словами")
            return data
        data.extend(ret_data)
        pg += 1
        if pg == ret_pages:
            print(f'Загружено {len(data)} вакансий')
            return data

def write_data(data:str) -> bool:

    try:
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Ошибка при записи в файл "{OUTPUT_FILENAME}": "{repr(e)}"')
        return False
    print(f'В файл "{OUTPUT_FILENAME}" выведено {len(data)} записей')
    return True

def main():

    data = request_data("Flask Django")

    if data == None or len(data) == 0: return

    write_data(data)

if __name__ == "__main__":
    main()