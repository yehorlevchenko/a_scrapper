This is a scraper that gets data from search suggestions. Made as a test assignment.

##### Usage:
1. pip3 install -r requirements.txt 
2. run scraper.py
_Sqlite database is populated for usage, no actions required._


##### Technical grounding:
Since JSON data can be acquired from the source, there is no point in interacting with web ui. It is more convenient to make direct API requests.


##### Flow:
1. Check if DB is populated with all possible character combinations ("queries"). Populate if empty.
2. Check DB if each query was scraped before. If all queries were scraped OR all queries were not scraped - reset and restart scraping. If part of queries were scraped - continue from the last scraped.
3. Main loop. Get first X queries from list and scrape them asynchroniously. Remove requested queries from the list.
4. On respond, unpack the data and save it to the DB.


##### Possible improvements:
* Using random headers to avoid ban;
* Using random time intervals between requests;
