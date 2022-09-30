import requests
import json



collected_data = []
def do_search():
    total_download_count = 0
    total_text_download_count = 0
    for page_idx in range(START_PAGE, MAX_PAGE_NUMBER, MAX_PAGE_SIZE):
        req_body = search_body
        req_body["page"]["from"] = page_idx
        citation_count, download_count, text_download_counts = do_search_request(req_body)
        total_text_download_count += text_download_counts
        total_download_count += download_count
        if total_text_download_count>2000:
            break
        #    if citation_count < MAX_PAGE_SIZE:
        #        break
    with open('collected_data.json', 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=4)

    print("Total downloaded count = "+str(total_download_count))
    print("Total text downloaded count = "+str(total_text_download_count))

def retriable_request(request):
    max_attempt = 2
    retry_attempt = 0
    resp = request() 
    while (not resp.status_code == 500) and retry_attempt <= max_attempt:
        resp = request()
        retry_attempt+=1
        limit_remaining = int(resp.headers["x-ratelimit-remaining"])
        if limit_remaining <= 0:
            print("rate Limited till "+ str(resp.headers["x-ratelimit-reset"]))
            break
    return resp

def do_search_request(search_body):
    request = lambda : requests.post(SEARCH_URL, data=json.dumps(search_body), headers = headers)
    resp = retriable_request(request)
    if(resp.status_code == requests.codes.ok):
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
    else:
        print(resp.status_code)
        print(resp.text)
    return


BASE_NTRS_URL = "https://ntrs.nasa.gov/api"
SEARCH_URL = BASE_NTRS_URL + "/citations/search"
MAX_PAGE_SIZE = 100
MAX_PAGE_NUMBER = 600000
START_PAGE = 6000
search_body = {
    "page": {
        "size": MAX_PAGE_SIZE,
        "from": START_PAGE
    },
    "sort": {
        "field": "id",
        "order": "asc"
    },
}

# keyword_search_body = {
#     "keyword": [
#         "plasma"
#     ],
#     "page": {
#         "size": MAX_PAGE_SIZE,
#         "from": 0
#     },
#     "sort": {
#         "field": "id",
#         "order": "dsc"
#     },
# }
headers = {"Content-Type": "application/json"}
ids_seen = set()

do_search()





