import urllib.parse
import requests
import fileinput
import re
import urllib.request
import os
from bs4 import BeautifulSoup
from Book import Book
import sys
from datetime import date


class Web_Scraper:

    def __init__(self, url_path):
        self.products_url = url_path + "products/"
        self.img_url = url_path + "wp-content/uploads/"
        self.current_page = None
        self.book_queue = []
        self.current_book = None
        self.product_number = 0

    """fills self.book_queue with book titles from file"""
    def get_books(self, file):
        f = open(file, encoding='utf-8')
        for b in f.readlines():
            b = re.sub("\s", "-", b)
            self.book_queue.append(b)
        f.close()


    def search_for_book(self, book_title):
        b = re.sub("-", " ", book_title)
        self.current_book = Book(b, ("%0.5d" % self.product_number))
        self.product_number += 1
        if (self.fetch_book_page(book_title) == 200):
            self.parse_page(book_title)
            self.download_image(book_title, self.current_book.product_number)


    def fetch_book_page(self, book_title):
        """Fetch a url and store page.

        :param path string the (absolute) url to fetch.
        :return None
        """
        print(book_title)
        r = requests.get(self.products_url + book_title)
        if r.status_code != 200:       # exit if status code other than 200
             print("Status Code of response of", r.url, "is", r.status_code)
             if r.status_code == 404:
                 print("Page not found. Check book title manually")
             return None

        cType = r.headers.get('Content-Type')
        if 'text/html' not in cType:
            print("Not HTML")
            return None

        self.current_page = r.text
        r.close()
        return r.status_code

    def parse_page(self, book_title):
        try:
            html = BeautifulSoup(self.current_page, "html.parser")
        except TypeError as e:
            print(e.with_traceback())
            return

        for a in html.select("a"):
            if "book-author" in a["href"]:
                author = a.text
                self.current_book.author = author
            if "publisher" in a["href"]:
                publisher = a.text
                self.current_book.publisher = publisher
            if "volumes" in a["href"]:
                volumes = a.text
                self.current_book.volumes = volumes
            """
            if "product-category" in a["href"]: # Problem: Ganze Liste aus der navbar wird gedruckt
                category = a.text
                print("Kategorie: " + category)
            """
        for img in html.select("img"):
            if img.has_attr("alt"):
                for word in img["alt"].split():
                    if word in self.current_book.title:
                        if img.has_attr("data-large_image"):
                            self.current_book.picture_link = img["data-large_image"]
                            break
                        elif self.current_book.picture_link == "":
                            self.current_book.picture_link = img["src"]
                            

        for td in html.select("td"):
            try:
                if "product_weight" in td["class"]:
                    weight = td.text
                    self.current_book.weight = weight
            except KeyError:
                pass

    def download_image(self, title, product_number):
        """ downloads an image with given path, creates a directory named title if non existent, 
        and saves image with "title + count"""
        dir_path = "img\\"
        file_path = dir_path + title + ".jpg"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        r = requests.get(self.current_book.picture_link)
        with open(file_path, "wb") as file:
            file.write(r.content)
        self.current_book.picture_link_on_moonlight = sys.argv[2] + str(date.today().year) + "/" + date.today().strftime("%m") + "/" + title + ".jpg"
    
if __name__ == '__main__':
    usage = "WebScraper.py takes 3 arguments: the URL of the website to scrape books from (e.g. \"http://www.google.com/\"), " \
            "the directory where the book images will be placed (e.g. \"http://my-website.com/static/img/\"), " \
            "the name of the file with the book titles to search for (e.g. \"books.txt\")." \
            "The results of the scraping will be printed to booklist.csv."
    if len(sys.argv) != 4:
        print(usage)
        exit()
    s = Web_Scraper(sys.argv[1])
    s.get_books(sys.argv[3])
    for book in s.book_queue:
        s.search_for_book(book)
        f = open("booklist.csv", "a", encoding='utf-8')
        print(s.current_book.print_book(), file=f)
    input()
