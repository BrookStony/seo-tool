import urllib.parse
import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (name, value) in attrs:
                    if name == "href":
                        self.links.append(value)
        elif tag == "meta":
            if len(attrs) == 0:
                pass
            else:
                for (name, value) in attrs:
                    if name == "name":
                       print(value)
        # elif tag == "title":
        #     print("title: " + )

def get(url, params):
    header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
             "Accept": "text/plain"}
    data = urllib.parse.urlencode(params).encode(encoding='UTF8')
    req = urllib.request.Request(url, data, headers=header)
    response = urllib.request.urlopen(req)
    content = response.read()
    print(response)
    # print(content)
    print(content.decode('utf8'))
    hp = MyHTMLParser()
    hp.feed(content.decode('utf8'))
    hp.close()
    print(hp.links)

get("https://www.ibm.com/cn-zh/", {})