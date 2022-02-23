import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from googlesearch import search

def read_url(url):
    try:       
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = Request(url, headers=headers)
        res = urlopen(request)
        time.sleep(0.3)
        html = res.read()
        soup = BeautifulSoup(html,'html.parser')
    except HTTPError as e:
        err = e.read()
        code = e.getcode()
        print(err)
        print(code)
    return soup


query = "automotive hacking"
my_results_list = []
for i in search(query,        # The query you want to run
                tld = 'com',  # The top level domain
                lang = 'en',  # The language
                num = 10,     # Number of results per page
                start = 0,    # First result to retrieve
                stop = None,  # Last result to retrieve
                pause = 2.0,  # Lapse between HTTP requests
               ):
    my_results_list.append(i)
    print(i)