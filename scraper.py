import asyncio
import schedule
import time
import logging
from suggestion_scraper import querystack

QUERY_PER_TICK = 5
CHECK_TIME = 10  # Seconds between requests
DB_NAME = "suggestion.db"

logging.basicConfig(
    filename='scrapper.log',
    level=logging.INFO,
    format='%(asctime)-15s %(message)s'
)


loop = asyncio.get_event_loop()
query_stack = querystack.QueryStack(QUERY_PER_TICK, DB_NAME)
query_stack.get_queries()
query_stack.process_queries(loop)


def method_wrapper(method, *args):
    method(*args)


# Schedule requests
schedule.clear()
schedule.every(CHECK_TIME).seconds.do(method_wrapper, query_stack.process_queries, loop)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(CHECK_TIME)
