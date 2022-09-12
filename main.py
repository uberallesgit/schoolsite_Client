import json

import requests
from bs4 import BeautifulSoup as bs
import re
import unicodedata as ud

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64; x64;rv: 104.0) Gecko / 20100101 Firefox / 104.0"
}



class Client:

    def load_page(self):
        url = "https://perv.mya5.ru/uchitelya"
        res = session.get(url=url)
        res.raise_for_status()
        return res.text


    def parse_page(self,text: str):
        soup = bs(text,"lxml")
        container = soup.select("div.component.component-html") or soup.select("div.component.component-button")
        self.counter = 0
        self.data = []
        for block in container[1:-6]:
            self.parse_block(block=block)

            self.data.append(
                {
                "name": self.name,
                "status": self.status,
                "education": self.education,
                "experience": self.experience,
                "qualification": self.qualification
                }
                )


        # print(self.data)



    def parse_block(self,block):
        self.name_test = block.find("strong")
        if self.name_test is not None:
            # print(self.counter, self.name.text)
            try:
                # self.status = " ".join(self.name_test.parent.text.split()).split("-")[1]
                self.name = " ".join(" ".join(block.find_all("span")[1].text.split("-")).replace("\n"," ").strip().split()[:3]).replace("\xa0","").replace("\u2060","")
                self.status = " ".join(" ".join(block.find_all("span")[2].text.split("-")).replace("\n"," ").strip().split()[3:]).replace("\xa0","").replace("\u2060","")
                self.education = " ".join(block.find_all("span")[3].text.split("-")).replace("\n"," ").strip().replace("\xa0","").replace("\u2060","")
                if "Педагогический" in self.education:
                    self.education = " ".join(block.find_all("span")[2].text.split("-")).replace("\n"," ").strip().replace("\xa0","").replace("\u2060","")

                self.experience = " ".join(block.find_all("span")[4].text.split("-")).replace("\n"," ").strip().replace("\xa0","").replace("\u2060","")
                if "Образование:" in self.experience:
                    self.experience =" ".join(block.find_all("span")[6].text.split("-")).replace("\n", " ").strip().replace("\xa0","").replace("\u2060","")

                self.qualification = " ".join(block.find_all("span")[7].text.split("-")).replace("\n"," ").strip().replace("\xa0","").replace("\u2060","")
                if "категория" not in self.qualification:
                    self.qualification = "-"
                self.chargement = block.find_all("span")[7].text.replace("\xa0","").replace("\u2060","")
                if "Классное" not in self.chargement:
                    self.chargement = "-"
                else:
                    self.chargement = block.find_all("span")[7].text[-5:].replace(" ","")+" класс"

            except Exception as ex:
                pass
                # print(ex)
            # print(self.counter,self.name,self.chargement)

        self.counter += 1




    def dump_json(self,list_):
        with open("teachers.json","w") as file:
            try:
                json.dump(list_,file, indent=4,ensure_ascii=False)
            except Exception as ex:
                print(ex)




    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        self.dump_json(list_=self.data)





if __name__ == '__main__':

    parser = Client()
    parser.run()



