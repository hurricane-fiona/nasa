import json

import NTRSClient

START_PAGE = 0
METADATA_DIR = "../metadata/"
METADATA_ID_TRACKING_FILE = ".metadata_id_tracking"
METADATA_PAGE_TRACKING_FILE = ".metadata_page_tracking"
MAX_PUBLLICATION_YEAR = 2022

def get_all_articles_metadata():
    citation_already_downloaded = read_tracked_metadata_ids()
    fromYear, toYear, page_start, fetch_size = read_page_metadata()
    page_start = get_next_page_start(page_start, fetch_size)
    fromYear, toYear = get_next_years(fromYear, toYear)
    while toYear <= MAX_PUBLLICATION_YEAR:
        total_articles_downloaded_for_year = get_articles_by_year(fromYear, toYear, page_start,
                                                       citation_already_downloaded)
        print("{} Articles downloaded for {} to {}".format(total_articles_downloaded_for_year,
                                                           fromYear, toYear))
        fromYear = toYear
        toYear = toYear + 1
        page_start = 0


"""
@param fromYear format YYYY. the year that will be used for "gt" publication date
@param toYear format YYYY. the year that will be used for "lte" publication date
"""
def get_articles_by_year(fromYear, toYear, page_start, citation_already_downloaded):
    req_body = NTRSClient.set_publication_year(fromYear, toYear, NTRSClient.get_search_request())
    print("Fetching Articles: {} < Publish_date <= {}".format(fromYear, toYear))
    return get_articles_metadata_for_search_body(req_body, page_start, fromYear, toYear,
                                          citation_already_downloaded)

def get_articles_metadata_for_search_body(req_body, page_start, fromYear, toYear,
                                          citation_already_downloaded):
    total_articles_downloaded = 0
    while page_start < NTRSClient.MAX_PAGE_NUMBER:
        print("Fetching {} to {} Articles".format(str(page_start),
                                                                  int(page_start) + int(
            NTRSClient.MAX_PAGE_SIZE)))
        req_body = NTRSClient.set_from_page(page_start, req_body)
        citations = NTRSClient.do_search_request1(req_body)
        fetch_size = len(citations)
        total_articles_downloaded += fetch_size
        for citation in citations:
            citation_id = citation["id"]
            if not citation_id in citation_already_downloaded:
                save_metadata(citation)
                write_tracked_metadata_id(citation_id)
                citation_already_downloaded.add(citation_id)

        write_page_metadata(fromYear, toYear, page_start, fetch_size)
        page_start = get_next_page_start(page_start, fetch_size)
        if fetch_size < NTRSClient.MAX_PAGE_SIZE:
            print("No more articles for search criteria. Curr fetch size="+str(fetch_size))
            break
    return total_articles_downloaded

def make_citation_filename(citation):
    citation_id = str(citation["id"]).strip()
    return citation_id + ".json"

def save_metadata(citation):
    with open(METADATA_DIR + make_citation_filename(citation), "w") as f:
        json.dump(citation, f, indent=4)

def get_next_years(fromYear, toYear):
    if int(fromYear) == -1:
        return 1900, 1905
    return int(fromYear), int(toYear)

def get_next_page_start(curr_page_start, curr_fetch_size):
    curr_page_start = int(curr_page_start)
    curr_fetch_size = int(curr_fetch_size)

    if(curr_page_start == -1): return START_PAGE
    else: return curr_page_start+curr_fetch_size

def write_page_metadata(fromYear, toYear, page_idx, fetch_size):
    with open(METADATA_DIR+METADATA_PAGE_TRACKING_FILE, "a") as f:
        f.write(str(fromYear) + "," + str(toYear) + "," + str(page_idx) + "," + str(fetch_size) + "\n")

def read_page_metadata():
    page_start = -1
    fetch_size = -1
    fromYear = -1
    toYear = -1
    try:
        with open(METADATA_DIR+METADATA_PAGE_TRACKING_FILE, "r") as f:
            page_info = f.readline()
            while(page_info):
                fromYear, toYear, page_start, fetch_size = page_info.strip().split(",")
                page_info = f.readline()
    except FileNotFoundError as ex:
        print("IGNORED----->"+str(ex)+"<--------IGNORED")
        pass
    # return last page_start that has already been pulled
    # if there is  nothing read yet, we return page_start== -1 to indicate nothing is read
    return fromYear, toYear, page_start, fetch_size

def read_tracked_metadata_ids():
    ids = set()
    try:
        with open(METADATA_DIR+METADATA_ID_TRACKING_FILE, "r") as f:
            citation_id = f.readline()
            while(citation_id):
                citation_id = citation_id.strip()
                ids.add(citation_id)
                citation_id = f.readline()
    except FileNotFoundError as ex:
        # no metadata tracking file exists so assume its our first time
        print(ex)
        pass

    return ids

def write_tracked_metadata_id(citation_id):
    with open(METADATA_DIR+METADATA_ID_TRACKING_FILE, "a") as f:
        f.write(str(citation_id) + "\n")

def do_search():
    total_download_count = 0
    total_text_download_count = 0
    #for page_idx in range(START_PAGE, MAX_PAGE_NUMBER, MAX_PAGE_SIZE):
    #    req_body = search_body
    #    req_body["page"]["from"] = page_idx
    #    citation_count, download_count, text_download_counts = do_search_request(req_body)
    #    total_text_download_count += text_download_counts
    #    total_download_count += download_count
    #    if total_text_download_count>2000:
    #        break
        #    if citation_count < MAX_PAGE_SIZE:
        #        break
    #with open('collected_data.json', 'w', encoding='utf-8') as f:
        #json.dump(collected_data, f, ensure_ascii=False, indent=4)

    print("Total downloaded count = "+str(total_download_count))
    print("Total text downloaded count = "+str(total_text_download_count))

def test_read_tracked_metadata_ids():
    ids = read_tracked_metadata_ids()
    print(ids)

def test_write_tracked_metadata_id():
    write_tracked_metadata_id(1234)

def test_write_read_id_metadata_tracking():
    test_write_tracked_metadata_id()
    test_read_tracked_metadata_ids()

def test_write_page_metadata():
    write_page_metadata(1900, 1905, 0, 100)

def test_read_page_metadata():
    print(read_page_metadata())

def test_write_read_page_metadata():
    write_page_metadata(1900, 1905, 0, 100)
    p = get_next_page_start(0, 100)
    write_page_metadata(1900, 1905, p, 100)
    lfy, lty, p, f= read_page_metadata()
    print((lfy, lty, p,f))
    print(get_next_page_start(p, f))

if __name__ == '__main__':
    get_all_articles_metadata()
