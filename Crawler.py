import sys
import re
from bs4 import BeautifulSoup
import time
import urllib.request
import urllib.parse 
#total crawled links


def Crawler(base_url, keyphrase):
    total_links = 0
    notseen_url =[base_url]      #url that has to be visited
    present = 1                 #present level of the nodes
    nextl = 0                   #next level of the nodes
    count = 0
    seen_url =[]         #list of url visited
    main_page = "http://en.wikipedia.org/wiki/Main_Page"    #links of main page should be folllowed
    eng_page = "http://en.wikipedia.org/wiki/"          #links  of English pages only for prefix
    depth = 1           #depth of the crawled links
    colon = ":" 
    hashtag = "#"
    crawled = set()             #set of total links crawled
    patternmatch = re.compile(re.escape(eng_page))      #string pattern with which the page should start
    pattern = re.compile(keyphrase, re.IGNORECASE)      # string pattern to implement ignore if not contain relevant pattern  
    link_count = 0                          #count of links visited
    
    while len(notseen_url)>0 and depth<6:
        if depth ==6:
            exit(0)
            
        while present != 0:
            if len(crawled)>=1000:
                exit(0)
            try:
                #from the base url start crawling with a gap of 1 second
                time.sleep(1)
                # get elements from the start of the queue
                response_text = urllib.request.urlopen(notseen_url[0]).read()
            except:    
                print("Sorry unable to process your request")
            #creating object
            #total_links = len(notseen_url)
            soup1 = BeautifulSoup(response_text)
            can_link = soup1.find('link', rel="canonical")  # canonical link checking and avoid duplication
            present = present -1                                #pops links one by one
            #total_links = len(notseen_url)
            notseen_url.pop(0)
            href_canonical = can_link['href']
            text = soup1.get_text()
            if keyphrase != "" and pattern.search(text) is None:
                print("keyphrase not present in link popped")
                continue
            if href_canonical in crawled:
                continue
            crawled.add(href_canonical)             #removes url after it is visited
            count = len(crawled)                    #counts the crawled links
            print(count)
            link_count = link_count + 1
            '''
            for printing output on a text file which can be viewed in the txt file
            '''
            f = open("keyphrase_crawler1.txt","w+")
            for i,link in enumerate(list(crawled)):
                f.write("{} \t {} \n".format(i+1,link))
            f.close()

            #get links from the document
            links = soup1.find_all('a', href=True)
            for link in links:
                modified_href = link['href']
                try:
                    if colon not in modified_href and hashtag not in modified_href:
                        modified_href = urllib.parse.urljoin(base_url, modified_href)
                        cond1 = modified_href not in seen_url
                        cond2 = modified_href not in notseen_url
                        cond3 = patternmatch.match(modified_href)
                        cond4 = modified_href != main_page
                        if cond1 and cond2 and cond3 and cond4 :
                            notseen_url.append(modified_href)
                            seen_url.append(modified_href)
                    else:
                        continue
                except:
                    continue
        link_count = 0
        
        nextl = len(notseen_url)        #next set of nodes to be parsed
        total_links = nextl
        
        #modify depth variables    
        if present == 0:
            present = nextl
            print("All links upto depth %s crawled"%depth)
            print ("length is %s"%total_links)
            nextl = 0
            depth = depth + 1
    return set(crawled)
                 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Please enter seed and keyphrase(optional)")
    else:
        a = sys.argv[1]

    if len(sys.argv) > 2:
        b = sys.argv[2]
    else:
        b=""
    Crawler(a,b)