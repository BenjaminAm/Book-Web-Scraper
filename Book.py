class Book:

    def __init__(self, title, product_number, author = "", publisher = "", volumes = "", picture_link = "", weight = "", picture_link_on_moonlight = ""):
        self.title = title
        self.product_number = product_number
        self.author = author
        self.publisher = publisher
        self.volumes = volumes
        self.picture_link = picture_link
        self.picture_link_on_moonlight = picture_link_on_moonlight
        self.weight = weight

    def print_book(self):
        return self.title + ", " + self.product_number + ", Autor, " + self.author + ", 1, 1, Verlag," + self.publisher + ",1,1, Bände," + self.volumes + ",1,1, " + self.weight + ", " + self.picture_link_on_moonlight