import bs4 as bs
from chrome_driver import get_page
        
class LotteryGame:
    def __init__(self, table, id='', nums1='', nums2='', date='', time=''):
        self.table = table
        self.id = id
        self.nums1 = nums1
        self.nums2 = nums2
        self.date = date
        self.time = time

    def __str__(self):
        return f"{self.table} {self.date} {self.time} - {self.nums1}"

class LotteryResultsCollector:
    def __init__(self):
        self.results = []

    def add_result(self, game_result):
        self.results.append(game_result)

    def insert_multiple_records(self, conn):
        #group the results by table name
        table_results = {}
        for result in self.results:
            if result.table is None:
                raise ValueError("Table name not specified for game result")
            
            table_name = result.table

            if table_name not in table_results:
                table_results[table_name] = []

            table_results[table_name].append(result)

        #craete a cursor object to interact with the database
        cursor = conn.cursor()

        #insert all the collected results into the appropriate tables
        for table_name, results in table_results.items():
            query = f"INSERT INTO {table_name} (id, nums1, date, time"
            values = [(result.id, result.nums1, result.date, result.time) for result in results]

            if table_name in ["lottoplus", "ekstrapremia", "multimulti"]:
                query += ", nums2"
                values = [(result.id, result.nums1, result.date, result.time, result.nums2) for result in results]

            query += ") VALUES (%s, %s, %s, %s"
            placeholders = "%s, %s, %s, %s" if table_name in ["lottoplus", "ekstrapremia", "multimulti"] else "%s, %s, %s, %s, %s"
            query += placeholders + ")"
            
            cursor.executemany(query, values)

        #commit the transaction and close the cursor
        conn.commit()
        cursor.close()

def scrap_results(url: str):
    result_collector = LotteryResultsCollector()
    print(f"Scraping url: {url}")
    page = get_page(url)
    page = bs.BeautifulSoup(page, "html.parser")
    for code in page.find_all("div", class_="game-main-box skip-contrast"):  
        for row in code.find_all("div", class_="result-item"):
            game = row.find("p", class_="result-item__name").get_text().strip().replace(" ","").lower()
            if game in ["lotto", "eurojackpot", "multimulti", "ekstrapensja", "minilotto", "kaskada"]:
                result = LotteryGame(table=game)
                result.date = code.find("p", class_="sg__desc-title").get_text().strip()
                result.time = result.date[-5:].replace(":","") if ":" in result.date else None
                result.date = "".join(result.date.split(",")[1].strip().split(".")[::-1])
                result.id = row.find("p", class_="result-item__number").get_text().strip()
                for num in row.find_all("div", class_="scoreline-item"):
                    result.nums1 += num.get_text().strip() + ","
                result.nums1 = result.nums1.strip(",")    
                if result.table == "multimulti":
                    result.nums2 = row.find("div", class_="scoreline-item circle special-multi").get_text().strip()
            elif game in ["lottoplus", "ekstrapremia"]:
                for num in row.find_all("div", class_="scoreline-item"):
                    result.nums2 += num.get_text().strip() + ","
                result.nums2 = result.nums2.strip(",")
            else:
                continue
        result_collector.add_result(result)
    return result_collector

if __name__ == "__main__":
    scrap_results("https://www.lotto.pl/wyniki")