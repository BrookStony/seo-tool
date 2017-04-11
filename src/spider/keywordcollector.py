from bs4 import BeautifulSoup
import codecs
import urllib.parse
import urllib.request
import jieba
import re

class KeywordCollector():

    collect_url_max = 500
    exclude_words_map = {'jQuery', 'if', 'var', 'function', 'width', 'and', ''}
    collecting_urls_map = {}
    collected_urls_map = {}
    keywords_map = {}
    collect_time = ''
    collect_save_path = ''

    def __init__(self, collect_save_path, collect_time):
        try:
            self.collect_save_path = collect_save_path
            self.collect_time = collect_time
            cu_file = codecs.open(collect_save_path + "\collecting_urls_" + collect_time + ".csv", 'r', 'utf-8')
            for line in cu_file.readlines():
                line = line.strip("\n")
                splits = line.split(",")
                if len(splits) == 2:
                    self.collecting_urls_map[splits[0]] = int(splits[1])
            print("<init> collecting_urls_count: " + str(len(self.collecting_urls_map)))

            cdu_file = codecs.open(collect_save_path + "\collected_urls_" + collect_time + ".csv", 'r', 'utf-8')
            for line in cdu_file.readlines():
                line = line.strip("\n")
                splits = line.split(",")
                if len(splits) == 2:
                    self.collected_urls_map[splits[0]] = (splits[1] == 'True')
            print("<init> collected_urls_count: " + str(len(self.collected_urls_map)))

            keywords_file = codecs.open(collect_save_path + "\keywords_" + collect_time + ".csv", 'r', 'utf-8')
            for line in keywords_file.readlines():
                line = line.strip("\n")
                splits = line.split(",")
                if len(splits) == 2:
                    self.keywords_map[splits[0]] = int(splits[1])
            print("<init> keywords_count: " + str(len(self.keywords_map)))

            cu_file.close()
            cdu_file.close()
            keywords_file.close()

        except Exception as e:
            print(e)

    def collect_website(self, domain, url, params, domain_filters, path_filters):
        self.collect(domain, url, params, domain_filters, path_filters)
        self.write_files()

        urls = []
        for url in self.collecting_urls_map:
            if url.endswith('.pdf'):
                continue
            urls.append(url)
        if len(self.collected_urls_map) < self.collect_url_max:
            for url in urls:
                if 'cn' in url or 'zh' in url:
                    if None == self.collected_urls_map.get(url):
                        self.collect(domain, url, params, domain_filters, path_filters)
                        # del(self.collecting_urls_map[url])
                        self.write_files()

        urls.clear()
        for url in self.collecting_urls_map:
            if url.endswith('.pdf'):
                continue
            urls.append(url)
        if len(self.collected_urls_map) < self.collect_url_max:
            for url in urls:
                if 'cn' in url or 'zh' in url:
                    if None == self.collected_urls_map.get(url):
                        self.collect(domain, url, params, domain_filters, path_filters)
                        # del(self.collecting_urls_map[url])
                        self.write_files()

    def collect(self, domain, url, params, domain_filters, path_filters):
        print("<collect> url: " + url)
        try:
            self.collected_urls_map.setdefault(url, True)

            header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept": "text/plain"}
            data = urllib.parse.urlencode(params).encode(encoding='UTF8')
            req = urllib.request.Request(url, data, headers=header)
            response = urllib.request.urlopen(req)
            content = response.read()

            soup = BeautifulSoup(content.decode('utf8'))
            page_title = soup.title.string
            meta_keywords = ''
            meta_description = ''

            # 分析meta标签获取页面keywords和description
            meta_list = soup.find_all('meta')
            for tag in meta_list:
                if 'name' in tag.attrs:
                    if tag.attrs['name'].lower() == "keywords":
                        meta_keywords = tag.attrs['content']
                    elif tag.attrs['name'].lower() == "description":
                        meta_description = tag.attrs['content']

            # 分析链接
            u_protocol, rest = urllib.parse.splittype(url)
            u_domain, rest = urllib.parse.splithost(rest)

            link_list = soup.find_all('a')
            for tag in link_list:
                # print(tag.get_text())
                if 'href' in tag.attrs:
                    link = tag.attrs['href']
                    # print("href=" + link)
                    if link:
                        if 'mailto:' in link or 'tel:' in link:
                            continue
                        if 'javascript:' in link or '#' == link:
                            continue
                        sp_url, sp_query = urllib.parse.splitquery(link.strip())
                        # 相对路径URL补全协议和domain
                        if str(sp_url).startswith("//"):
                            sp_url = u_protocol + ":" + sp_url
                        elif str(sp_url).startswith("/"):
                            sp_url = u_protocol + "://" + u_domain + sp_url
                        elif ':' not in sp_url:
                            if url.endswith("/"):
                                sp_url = url + sp_url
                            else:
                                sp_url = url + "/" + sp_url

                        if None == self.collected_urls_map.get(sp_url):
                            u_protocol, rest = urllib.parse.splittype(sp_url)
                            u_domain, rest = urllib.parse.splithost(rest)
                            flag = False
                            for f in domain_filters:
                                if f in u_domain:
                                    flag = True
                                    break

                            if flag:
                                if len(path_filters) > 0:
                                    flag = False
                                for f in path_filters:
                                    if f in sp_url:
                                        flag = True
                                        break

                            if flag:
                                url_times = self.collecting_urls_map.get(sp_url)
                                if url_times:
                                    url_times += 1
                                    self.collecting_urls_map[sp_url] = url_times
                                else:
                                    self.collecting_urls_map.setdefault(sp_url, 1)

            # 统计关键词
            # page_text = soup.body.get_text()
            # self.stat_keywords(url, page_title + "\n" + meta_keywords + "\n" + meta_description + "\n" + page_text)
            [script.extract() for script in soup.findAll('script')]
            [style.extract() for style in soup.findAll('style')]
            soup.prettify()
            regex = re.compile("<[^>]*>")
            page_text = regex.sub('', soup.prettify())
            self.stat_keywords(url, page_text)
        except Exception as e:
            print(e)

    def stat_keywords(self, url, page):
        print("<stat_keywords> url: " + url)
        try:
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
                            print("word: " + word + ", word_times=" + str(word_times))
                            self.keywords_map[word] = word_times
                        else:
                            # print("word: " + word + ", word_times=1")
                            self.keywords_map.setdefault(word, 1)

            lines.clear()
        except Exception as e:
            print(e)

    def write_files(self):
        print("<write_files>")
        try:
            print("<write_files> collecting_urls_count: " + str(len(self.collecting_urls_map)))
            cu_file = codecs.open(self.collect_save_path + "\collecting_urls_" + self.collect_time + ".csv",
                                  'wb', 'utf-8')
            for (k, v) in self.collecting_urls_map.items():
                cu_file.write(k + "," + str(v) + "\n")

            print("<write_files> collected_urls_count: " + str(len(self.collected_urls_map)))
            cdu_file = codecs.open(self.collect_save_path + "\collected_urls_" + self.collect_time + ".csv",
                                   'wb', 'utf-8')
            for (k, v) in self.collected_urls_map.items():
                cdu_file.write(k + "," + str(v) + "\n")

            print("<write_files> keywords_count: " + str(len(self.keywords_map)))
            sorted(self.keywords_map.items(), key=lambda d: d[1])
            keywords_file = codecs.open(self.collect_save_path + "\keywords_" + self.collect_time + ".csv",
                                        'wb', 'utf-8')
            for (k, v) in self.keywords_map.items():
                keywords_file.write(k + "," + str(v) + "\n")

            cu_file.close()
            cdu_file.close()
            keywords_file.close()

        except Exception as e:
            print(e)

keyword_collector = KeywordCollector("D:\dev\python\seo-tool\out\KeywordCollector", "20170311")
# keyword_collector.init()
keyword_collector.collect_website("www.ibm.com", "https://www.ibm.com/cn-zh/", [], ['ibm'], [])
# keyword_collector.collect_website("www.ibm.com", "https://www.ibm.com/cn-zh/", [], ['ibm'],
#                                   ['analytics', 'middleware', 'software', 'cloud-computing', 'systems', 'services',
#                                    'security', 'cognitive', 'it-infrastructure', 'commerce', 'solutions'])