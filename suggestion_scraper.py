import asyncio
import aiohttp
import schedule
import time
import logging
from dbhandler import DBHandler

QUERY_PER_TICK = 5
CHECK_TIME = 10  # Seconds between requests
DB_NAME = "suggestion.db"

logging.basicConfig(
    filename='scrapper.log',
    level=logging.INFO,
    format='%(asctime)-15s %(message)s'
)


class QueryStack:
    def __init__(self):
        self.url = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)',
            'Connection': 'close'}
        self.query_step = 5
        self.items = []
        logging.info(f"Instance of QueryStack initiated")

    def get_queries(self):
        rows = db_handler.db_get_queries()
        self.items = [row[1] for row in rows]

    def process_queries(self):
        query_list = self.items[:QUERY_PER_TICK]
        self.items = self.items[QUERY_PER_TICK:]
        logging.info(f"QueryStack started processing queries {query_list}")
        for item in query_list:
            logging.info(f"QueryStack processing {item}")
            loop.run_until_complete(self.get_data(item))

    async def get_data(self, query):
        params = {'currentTheme': 'main', 'currentLocale': 'uk_UA', 'q': query}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers, params=params) as response:
                logging.info(f"QueryStack requested {query}")
                data = await response.json(content_type='text/html')
                logging.info(f"QueryStack received response for {query}")
                if data:
                    self.unpack_data(data, query)

    def unpack_data(self, data, query_name):
        records = [[suggestion, ] for suggestion in data['query']]
        if records:
            logging.info(f"QueryStack unpacked data from {query_name}")
            self.save_data(records, query_name)

    def save_data(self, records, query_name):
        if db_handler.db_insert_suggestion(records, query_name):
            logging.info(f"QueryStack saved {query_name} data to DB")
        else:
            logging.error(f"QueryStack FAILED to save {query_name} data to DB")


loop = asyncio.get_event_loop()
db_handler = DBHandler(db_name=DB_NAME)
db_handler.db_populate()
query_stack = QueryStack()
query_stack.get_queries()
query_stack.process_queries()


def method_wrapper(method):
    method()


# Schedule requests
schedule.clear()
schedule.every(CHECK_TIME).seconds.do(method_wrapper, query_stack.process_queries)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(CHECK_TIME)
