import aiohttp
import logging
from .dbhandler import DBHandler

logging.basicConfig(
    filename='scrapper.log',
    level=logging.INFO,
    format='%(asctime)-15s %(message)s'
)

class QueryStack:

    def __init__(self, query_size, db_name):
        self.url = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko)',
            'Connection': 'close'}
        self.query_size = query_size
        self.db_handler = DBHandler(db_name)
        self.db_handler.db_populate()
        self.items = []
        logging.info(f"Instance of QueryStack initiated")

    def get_queries(self):
        rows = self.db_handler.db_get_queries()
        self.items = [row[1] for row in rows]

    def process_queries(self, loop):
        query_list = self.items[:self.query_size]
        self.items = self.items[self.query_size:]
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
        if self.db_handler.db_insert_suggestion(records, query_name):
            logging.info(f"QueryStack saved {query_name} data to DB")
        else:
            logging.error(f"QueryStack FAILED to save {query_name} data to DB")
