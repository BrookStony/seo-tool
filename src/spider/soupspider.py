import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

class SoupSpider():

    def analyse(self, domain, url, params):
        """分析页面"""
        result = {}
        header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
             "Accept": "text/plain"}
        data = urllib.parse.urlencode(params).encode(encoding='UTF8')
        req = urllib.request.Request(url, data, headers=header)
        response = urllib.request.urlopen(req)
        content = response.read()
        # print(response)
        # print(content)
        # print(content.decode('utf8'))

        soup = BeautifulSoup(content.decode('utf8'))
        result['title'] = soup.title.string

        # 分析meta标签获取页面keywords和description
        meta_list = soup.find_all('meta')
        for tag in meta_list:
            print(tag.attrs)
            if 'name' in tag.attrs:
                if tag.attrs['name'] == "keywords":
                    result['keywords'] = tag.attrs['content']
                elif tag.attrs['name'] == "description":
                    result['description'] = tag.attrs['content']

        # 分析链接
        link_list = soup.find_all('a')
        for tag in link_list:
            print(tag.get_text())
            if 'href' in tag.attrs:
                print("href=" + tag.attrs['href'])

            # print("text=" + tag.string)

        print(soup.p)
        print(soup.a)
        # print(soup.find_all('a'))
        print(soup.find(id='link3'))
        print("====================================================================================================")
        print(soup.get_text())
        print("====================================================================================================")
        print(soup.find("body").get_text())

        return result

spider = SoupSpider()
result = spider.analyse("www.ibm.com", "http://www-31.ibm.com/ibm/cn/cognitive/outthink/", {})
# result = spider.analyse("www.ibm.com", "https://www.ibm.com/analytics/cn/zh/technology/", {})
# result = spider.analyse("www.ibm.com", "https://www.ibm.com/cn-zh/", {})
print("title: " + result['title'])
print("keywords: " + result['keywords'])
print("description: " + result['description'])