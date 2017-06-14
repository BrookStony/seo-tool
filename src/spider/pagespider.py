from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import jieba
import re

class PageSpider():

    keywords_map = {}

    def stat_keywords(self, url, params):
        print("<stat_keywords> url: " + url)
        try:
            jieba.load_userdict("D:\dev\python\seo-tool\conf\keyword_dict.txt")

            header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept": "text/plain"}
            data = urllib.parse.urlencode(params).encode(encoding='UTF8')
            req = urllib.request.Request(url, data, headers=header)
            response = urllib.request.urlopen(req)
            content = response.read()

            soup = BeautifulSoup(content.decode('utf8'))

            # 统计关键词
            # page_text = soup.body.get_text()
            # self.stat_keywords(url, page_title + "\n" + meta_keywords + "\n" + meta_description + "\n" + page_text)
            body = soup.body
            [script.extract() for script in body.findAll('script')]
            [style.extract() for style in body.findAll('style')]
            body.prettify()
            regex = re.compile("<[^>]*>")
            page = regex.sub('', body.prettify())

            lines = []
            split_lines = page.splitlines()
            for line in split_lines:
                line = line.strip()
                if '' != line:
                    lines.append(line)

            for line in lines:
                words = jieba.cut_for_search(line)
                for word in words:
                    if len(word) > 1:
                        word_times = self.keywords_map.get(word)
                        if word_times:
                            word_times += 1
                            # print("word: " + word + ", word_times=" + str(word_times))
                            self.keywords_map[word] = word_times
                        else:
                            # print("word: " + word + ", word_times=1")
                            self.keywords_map.setdefault(word, 1)

            lines.clear()

        except Exception as e:
            print(e)

    def sort_keywords(self, keywords_map):
        keywords = []
        keywords_list = []
        for (k, v) in keywords_map.items():
            keywords_list.append((k, v, len(k)))
        # 排序
        keywords_list.sort(key=lambda x: (x[2], x[1]), reverse=True)
        for words in keywords_list:
            print(words[0] + ": " + str(words[1]))
            # keywords.append(words[0])
        return keywords

page_spider = PageSpider()
# page_spider.stat_keywords("https://www-935.ibm.com/industries/cn-zh/banking/solutions/"
#                           "solution-consumer-insight.html", {})
page_spider.stat_keywords("http://www-03.ibm.com/software/products/zh/spss-statistics", {})
page_spider.sort_keywords(page_spider.keywords_map)
