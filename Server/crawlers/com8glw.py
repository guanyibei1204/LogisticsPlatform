from bs4 import BeautifulSoup
from crawler import Crawler

class Crawler8glw(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.HOST = "http://www.8glw.com/"
        self.prefix = "/main_info.asp?id=1&page="

    def uniform(self, page):
        soup = BeautifulSoup(page, "html.parser")   # lxml
        for li in soup.find(attrs = {"class": "list"}).find_all("li"):
            item = {"site": "8glw"}
            item["url"] = self.HOST + li.a.get("href")
            page = self.get(item["url"])
            soup = BeautifulSoup(page, "html.parser")   # lxml
            table = soup.find(attrs = {"class": "box"}).table
            item["description"] = table.text
            tds = table.find_all("tr")
            item["from"] = tds[4].td.text.strip()
            item["to"] = tds[5].td.text.strip()
            begin = tds[-3].td.text.strip().split('-')
            end = tds[-4].td.text.strip().split('-')
            item["date"], item["deadline"] = self.lifetime(begin, end)
            if item in self.data or self.exist(item):
                self.window -= 1
                continue
            self.data.append(item)