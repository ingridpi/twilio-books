# Twilio Bookish App

## Run the app

Setting up the environment

1. Change the directory to `Twilio Books App`
    ```
    cd 'Twilio Books App'
    ```
2. Create a virtual environment
    ```
    python3 -m venv app-env
    ```
3. Activate the virtual environment
    ```
    source app-env/bin/activate
    ```

4. Install the necessary dependencies
    ```
    pip install -r requirements.txt
    ```

Running the application

After having followed the steps of the previous section, run the command:
```
python3 app.py
```

Exposing the application

Once the app is running, to expose it on the internet, run the command:

```
ngrok http 8080
```

## Funcionality

The app main functionality is described to the user upon receiving an initial text, such as `hello`:

```

Welcome to Bookish!
To get a quote, text *quote*
To upload your reading library, send a csv file named *library_%.csv*
To retrieve information from your library, the available options are:
    *random*: Get a random book from your to-read list
    *book-%book_title%*: Information about the book
    *author - %author_name%*: Books from that author
To upload your reading schedule, send a csv file named *reading_%.csv*
To retrieve information from your reading schedule, the available options are:
    *today*: Get what you have pending to read until today
    *today-%book_title%*: Get what you have pending to read until today from a given book
    *complete*: Mark everything until today as read
    *complete-%book_name%*: Mark everything until today from the given book as read

```

The main functionality described above can be summarised in the following table:

| Text Format    | Description     | Example     |
| :------------- | :-------------- | :------------ |
| quote | Get a random quote from api.quotable.io | *quote* |
| **library_%.csv** | Send a file to upload the associated reading library | *library_ingrid.csv* |
| random | Get a random book from your reading library that you have not read yet | *random* |
| book-**%book_name%** | Get the book information from the book with name %book_name% | *book-throne of glass* |
| author-**%author_name%** | Get the list of books from the author with name %author_name% in your library | *author-victoria aveyard* |
| reading_%.csv | Send a file to upload the associated reading schedule | *reading_city_of_ashes.csv* |
| today | Get the chapters pending to be read up to today | *today* |
| today-**%book_name%** | Get the chapters pending to be read up to today from the book with name %book_name% | *today-city of ashes* |
| mark_complete | Mark the chapters pending until today as read | *complete* |
| complete-**%book_name%** | Mark the chapters pending until today as read from the book with name %book_name% | *complete-city of ashes* |


The files format should be:

**library_%.csv**

| Column Name | Description | Example |
| :------------- | :------------- | :------------- |
| Title | Book title (String) | *The Inexplicable Logic of My Life* |
| Author | Author name (String) | *Benjamin Alire Sáenz* |
| My Rating | Rating given to the book if the book has been read (Categorical: 1-5) | *4* |
| Average Rating | Average Rating provided by GoodReads (Float) | *4.14* |
| Number of Pages | Book length (Integer) | *452* |
| Date Read | If the book has been read, then the date should be added (YYYY/MM/DD) | *2020/12/29* |
| Exclusive shelf | Shelf the book belongs to (read, currently-reading, to-read) | *read* |


**reading_%.csv**

| Column Name | Description | Example |
| :------------- | :------------- | :------------- |
| Book | Book title (String) | *City of Ashes* |
| Date | Date the reading is scheduled (DD/MM/YYYY) | *22/08/2021* |
| Chapters | Begin Chapter - End Chapter (String) | *Prologue - 3* |
