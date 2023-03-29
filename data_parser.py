import bs4 as bs
from chrome_driver import get_page
from main import db_cur

class Result():
    def __init__(self, table):
        self.__table__ = table

    def __str__(self):
        return f"{self.__table__} {self.date} {self.time} - {self.nums1} / {self.nums2}"

    id = ''
    date = ''
    time = ''
    nums1 = ''
    nums2 = ''

    def insert_db(self):
        cur = db_cur()
        [a for a in dir(obj) if not a.startswith('__')]
        cur.execute(f'INSERT INTO {self.} ... ON CONFLICT DO NOTHING')


# def insert_db(): 
#    db_cur.execute('INSERT ... ON CONFLICT DO NOTHING/UPDATE')

def scrap_results(url):
    print(f"Scraping url: {url}")
    page = get_page(url)
    print(page)
    page = bs.BeautifulSoup(page, "html.parser")
    for code in page.find_all("div", class_="game-main-box skip-contrast"):  
        for row in code.find_all("div", class_="result-item"):
            name = row.find("p", class_="result-item__name").get_text().strip()
            if name in ["Lotto", "Eurojackpot", "Multi Multi", "Ekstra Pensja", "Mini Lotto", "Kaskada"]:
                result = Result(name.replace(" ", "").lower())
                result.date = code.find("p", class_="sg__desc-title").get_text().strip()
                result.time = result.date[-5:].replace(":","") if ":" in result.date else None
                result.date = "".join(result.date.split(",")[1].strip().split(".")[::-1])
                result.id = row.find("p", class_="result-item__number").get_text().strip()
                for i in row.find_all("div", class_="scoreline-item"):
                    result.nums1 += i.get_text().strip() + ","
                if result.table == "multimulti":
                    result.nums2 = row.find("div", class_="scoreline-item circle special-multi").get_text().strip()
            elif name in ["Lotto Plus", "Ekstra Premia"]:
                for i in row.find_all("div", class_="scoreline-item"):
                    result.nums2 += i.get_text().strip() + ","
            elif name in ["Super Szansa", "Keno"]:
                pass
            else:
                print(f'{name} game didnt match the data.')
        print(result)
        del result
