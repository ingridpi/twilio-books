from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from functions import *

app = Flask('books')


@app.route('/', methods=['GET'])
def init():
    outgoing = MessagingResponse()
    msg = outgoing.message()
    message = "Welcome to the Bookish app! To enable this service on WhatsApp, text: join collect-dried to +1 415 523 8886"
    msg.body(message)
    return str(outgoing)

@app.route('/book', methods=['POST'])
def book():
    incoming = request.values.get('Body', '').lower()
    outgoing = MessagingResponse()
    msg = outgoing.message()
    responded = False
    sender = request.values.get('From', '').lower()
    sender = sender.split(":")[1]

    media = int(request.values.get('NumMedia'))

    if media != 0:
        name = request.values.get('Body', '').lower()
        url = request.values.get('MediaUrl0')
        type = request.values.get('MediaContentType0')

        process_file(msg, name, url, type, sender)
        responded = True

    else:
        if 'quote' in incoming:
            quote(msg)
            responded = True

        elif 'random' in incoming:
            random(msg, sender)
            responded = True

        elif 'book' in incoming:
            title = incoming.split("-")[1]
            book_info(msg, title, sender)
            responded = True

        elif 'author' in incoming:
            author = incoming.split("-")[1]
            author_info(msg, author, sender)
            responded = True

        elif 'today-' in incoming:
            title = incoming.split("-")[1]
            get_book_today(msg, title, sender)
            responded = True

        elif 'today' in incoming:
            get_today(msg, sender)
            responded = True

        elif 'complete-' in incoming:
            title = incoming.split("-")[1]
            mark_book_complete(msg, title, sender)
            responded = True

        elif 'complete' in incoming:
            mark_complete(msg, sender)
            responded = True

    if not responded:
        hello(msg)

    return str(outgoing)


if __name__ == '__main__':
    init()
    app.run(debug=True, host='127.0.0.1', port=8080)
