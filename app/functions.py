import pandas as pd
import requests
import numpy as np
from datetime import datetime

books = {}
readings = {}

def init():
    add_book("+34689421612", "library_ingrid.csv")
    add_book("+34683583922", "library_clara.csv")
    add_reading("+34689421612", "reading_city_of_ashes.csv")
    add_reading("+34689421612", "reading_atomic_habits.csv")
    add_reading("+34683583922", "reading_city_of_ashes.csv")


def add_book(sender, filename):
    books[sender] = load_book(filename)


def load_book(filename):
    columns = ["Title", "Author", "My Rating", "Average Rating", "Number of Pages", "Date Read", "Exclusive Shelf"]
    data = pd.read_csv("./data/" + filename)
    data = data[columns]
    data["Date Read"] = pd.to_datetime(data["Date Read"])
    return data


def add_reading(sender, filename):
    info = load_reading(filename)

    if sender not in readings:
        readings[sender] = {}

    for elem in info["Book"].unique():
        data = info[info["Book"] == elem]
        data["Date"] = pd.to_datetime(data["Date"],  format='%d/%m/%Y')
        data = data.sort_values(by = "Date")
        readings[sender][elem.lower()] = data


def load_reading(filename):
    data = pd.read_csv("./data/" + filename)
    data["Pending"] = True
    return data


def hello(msg):
    message = "Welcome to Bookish! \nTo get a quote, text *quote* \nTo upload your reading library, send a csv file named *library_%.csv* \nTo retrieve information from your library, the available options are: \n\t*random*: Get a random book from your to-read list \n\t*book-%book_title%*: Information about the book \n\t*author - %author_name%*: Books from that author \nTo upload your reading schedule, send a csv file named *reading_%.csv* \nTo retrieve information from your reading schedule, the available options are: \n\t*today*: Get what you have pending to read until today \n\t*today-%book_title%*: Get what you have pending to read until today from a given book \n\t*complete*: Mark everything until today as read \n\t*complete-%book_name%*: Mark everything until today from the given book as read"
    msg.body(message)


def quote(msg):
    url = "https://api.quotable.io/random"
    req = requests.get(url)

    if req.status_code == 200:
        data = req.json()
        quote = "{} ({})".format(data["content"], data["author"])

    else:
        quote = "quote could not be found"

    msg.body(quote)


def random(msg, sender):
    if sender not in books:
        random = "no data found for the user"

    else:
        data = books[sender]
        unread = data[data["Exclusive Shelf"] == "to-read"]

        if unread.shape[0] > 0:
            book = unread.sample()
            title = book["Title"].values[0]
            author = book["Author"].values[0]
            pages = int(book["Number of Pages"].values[0])
            rating = book["Average Rating"].values[0]
            random = "*{}* \nAuthor: {} \nPages: {} \nAverage Rating: {}".format(title, author, pages, rating)

        else:
            random = "no unread books"

    msg.body(random)


def book_info(msg, title, sender):
    if sender not in books:
        book_info = "no data found for the user"

    else:
        data = books[sender]
        book = data[data["Title"].str.lower().str.startswith(title)]

        if book.shape[0] == 0:
            book_info = "the book was not found"

        else:
            title = book["Title"].values[0]
            author = book["Author"].values[0]
            pages = int(book["Number of Pages"].values[0])
            rating = book["Average Rating"].values[0]
            book_info = "*{}* \nAuthor: {} \nPages: {} \nAverage Rating: {}".format(title, author, pages, rating)

            date_read = book["Date Read"].dt.strftime("%d %b %Y").values[0]
            if not np.isnan(date_read):
                my_rating = book["My Rating"].values[0]
                book_info += "\nDate Read: {} \nMy Rating: {}".format(date_read, my_rating)

    msg.body(book_info)


def author_info(msg, author, sender):
    if sender not in books:
        author_info = "no data found for the user"

    else:
        data = books[sender]
        book = data[data["Author"].str.lower() == author]

        if book.shape[0] == 0:
            author_info = "the author was not found"

        else:
            author = book["Author"].values[0]
            author_info = "*{}*".format(author)

            for index, row in book.iterrows():
                title = row["Title"]
                rating = row["Average Rating"]
                author_info += "\n{} ({})".format(title, rating)

    msg.body(author_info)


def process_file(msg, name, url, type, sender):
    if type == 'text/csv':

        if name.startswith('library_'):
            response = requests.get(url)
            open(name, 'wb').write(response.content)
            add_book(sender, name)

            if sender in books:
                process_file = "new library added"

            else:
                process_file = "error occured when adding library"

        elif name.startswith('reading_'):
            response = requests.get(url)
            open(name, 'wb').write(response.content)
            add_reading(sender, name)
            process_file = "new reading added"

        else:
            process_file = "file name not allowed"

    else:
        process_file = "file extension not allowed"

    msg.body(process_file)


def get_book_today(msg, title, sender):
    if sender not in readings:
        today_info = "no data found for the user"

    else:
        data = readings[sender]

        if title not in data:
            today_info = "book not found in readings"

        else:
            data = readings[sender][title]
            today = np.datetime64('today')
            data = data[data["Date"] <= today]
            data = data[data["Pending"] == True]

            if len(data) == 1:
                title = data["Book"].values[0]
                chapters = data["Chapters"].values[0]
                today_info = "*{}*: {}".format(title, chapters)

            elif len(data) > 1:
                title = data["Book"].values[0]
                today_info = "*{}*".format(title)

                for index, row in data.iterrows():
                    date = row["Date"].date().strftime("%d %b")
                    chapters = row["Chapters"]
                    today_info += "\n\t{}: {}".format(date, chapters)

            else:
                today_info = "no readings pending"

    msg.body(today_info)


def get_today(msg, sender):
    if sender not in readings:
        today_info = "no data found for the user"

    else:
        data_dict = readings[sender]
        today_info = ""

        for title in data_dict:
            data = readings[sender][title]
            today = np.datetime64('today')
            data = data[data["Date"] <= today]
            data = data[data["Pending"] == True]

            if len(data) > 0:
                title = data["Book"].values[0]
                today_info += "*{}*".format(title)

                for index, row in data.iterrows():
                    date = row["Date"].date().strftime("%d %b")
                    chapters = row["Chapters"]
                    today_info += "\n\t{}: {}".format(date, chapters)

                today_info += "\n"

        if len(today_info) == 0:
            today_info = "no readings pending"

    msg.body(today_info)


def mark_book_complete(msg, title, sender):
    if sender not in readings:
        complete_info = "no data found for the user"

    else:
        count = 0
        data = readings[sender][title]
        today = np.datetime64('today')
        count += len(data[(data["Date"] <= today) & (data["Pending"] == True)])
        data.loc[(data["Date"] <= today) & (data["Pending"] == True), "Pending"] = False
        readings[sender][title] = data

        if count == 0:
            complete_info = "no reading entries were updated"
        elif count == 1:
            complete_info = "1 reading entry was updated"
        else:
            complete_info = "{} reading entries were updated".format(count)

    msg.body(complete_info)


def mark_complete(msg, sender):
    if sender not in readings:
        complete_info = "no data found for the user"

    else:
        data_dict = readings[sender]
        count = 0

        for title in data_dict:
            data = readings[sender][title]
            today = np.datetime64('today')
            count += len(data[(data["Date"] <= today) & (data["Pending"] == True)])
            data.loc[(data["Date"] <= today) & (data["Pending"] == True), "Pending"] = False
            readings[sender][title] = data

        if count == 0:
            complete_info = "no reading entries were updated"
        elif count == 1:
            complete_info = "1 reading entry was updated"
        else:
            complete_info = "{} reading entries were updated".format(count)

    msg.body(complete_info)
