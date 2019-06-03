import requests
import schedule
import time
from db_conn import DBhandler

URL = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)', 'Connection': 'close'}
CHECK_TIME = 0.1  # Minutes between requests

db_handler = DBhandler(db_name="suggestion.db")

schedule.clear()


def get_data(query="iph"):
    """Gets value from URL during session and calls save_stat()"""
    params = {'currentTheme': 'main', 'currentLocale': 'uk_UA', 'q': query}
    with requests.Session() as session:
        response = session.get(URL, headers=HEADERS, params=params).json()
        if response:
            unpack_data(response)
        else:
            print("Unable to get data from URL")


def unpack_data(data):
    records = [(suggestion,) for suggestion in data['query']]
    if records:
        save_data(records)


def save_data(records):
    """Posts provided data with to the DB"""
    db_handler.db_connect()
    if db_handler.db_insert_suggestion(records):
        print("Record")
    else:
        print("Fail")


# Schedule data update every X seconds
schedule.every(CHECK_TIME).minutes.do(get_data)

# Main loop
while 1:
    schedule.run_pending()
    time.sleep(CHECK_TIME/60)
