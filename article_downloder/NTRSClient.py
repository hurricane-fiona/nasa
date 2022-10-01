import requests
import json

BASE_NTRS_URL = "https://ntrs.nasa.gov"
SEARCH_URL = BASE_NTRS_URL + "/api/citations/search"
MAX_PAGE_SIZE = 100
MAX_PAGE_NUMBER = 600000


collected_data = []
headers = {"Content-Type": "application/json"}
ids_seen = set()

search_body = {
    "page": {
        "size": MAX_PAGE_SIZE,
        "from": 0
    },
    "sort": {
        "field": "id",
        "order": "asc"
    },
}
class WebException(Exception):
    def __init__(self, http_code, err_msg, rate_limit_remaining):
        super().__init__(err_msg + " RateLimitRemaining="+str(rate_limit_remaining))
        self.rate_limit_remaining = rate_limit_remaining
        self.http_code = http_code
        self.err_msg = err_msg

def set_from_page(start_page, search_body):
    search_body["page"]["from"] = start_page
    return search_body

def set_publication_year(fromYear, toYear, search_body):
    search_body["published"] = {}
    search_body["published"]["gt"] = str(fromYear)
    search_body["published"]["lte"] = str(toYear)
    search_body["published"]["format"] = "YYYY"
    return search_body

def get_search_request():
    body = search_body.copy()
    return body

def __retriable_request(request):
    max_attempt = 2
    retry_attempt = 0
    resp = request() 
    while (not resp.status_code == 500) and retry_attempt <= max_attempt:
        resp = request()
        retry_attempt+=1
        limit_remaining = __get_rate_limit_remaining(resp)
        if limit_remaining <= 0:
            print("rate Limited till "+ str(resp.headers["x-ratelimit-reset"]))
            break
    return resp

def __get_rate_limit_remaining(resp):
    return int(resp.headers["x-ratelimit-remaining"])

def __do_request(request):
    resp = __retriable_request(request)
    if(not resp.status_code == requests.codes.ok):
        limit_remaining = __get_rate_limit_remaining(resp)
        raise WebException(resp.status_code, resp.text, limit_remaining)
    return resp

def __parse_search_response(resp):
    search_resp = resp.json()
    citations = search_resp["results"]
    return citations

def do_search_request1(search_body):
    request = lambda : requests.post(SEARCH_URL, data=json.dumps(search_body), headers = headers)
    resp = __do_request(request)
    return __parse_search_response(resp)

def do_search_request(search_body):
    request = lambda : requests.post(SEARCH_URL, data=json.dumps(search_body), headers = headers)
    resp = __do_request(request)

    search_resp = resp.json()
    citations = search_resp["results"]
    download_count = 0
    text_download_counts = 0
    print("From {} to {} Articles found {}".format(str(search_body["page"]["from"]),
                                                 str(search_body["page"]["from"] +
                                                     MAX_PAGE_SIZE - 1),
                                                 str(len(citations))))
    #print(citations)
    for citation in citations:
        citation_id = citation["id"]
        assert(not citation_id in ids_seen)
        ids_seen.add(citation_id)
        downloadsAvailable = citation["downloadsAvailable"]
        if downloadsAvailable:
            download_count+=1
            downloads = citation["downloads"]
            if downloads:
                if len(downloads) > 1: print("{} Has more than 1 download".format(citation["title"]))
                for download in downloads:
                    download_links = download["links"]
                    if download_links.get("fulltext"):
                        collected_data.append(citation)
                        text_download_counts += 1
    print("Downloads available for "+str(download_count))
    print("Text Downloads available for "+str(text_download_counts))
    return len(citations), download_count, text_download_counts

def download(url):
    request = lambda: requests.get(BASE_NTRS_URL + url)
    return __do_request(request)

class Citations:
    def __init__(self, citations):
        self.citations = citations

    def get(self):
        return self.citations


#do_search()





