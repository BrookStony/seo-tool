import urllib.parse
import urllib.request
import http.cookiejar

from bs4 import BeautifulSoup
import json
import random
import threading
import webbrowser
from selenium import webdriver

import time

class SearchVisitsRobot():

    agents = ["Opera/9.27 (Windows NT 5.2; U; zh-cn)",
              "Opera/8.0 (Macintosh; PPC Mac OS X; U; en)",
              "Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0 ",
              "Opera/9.80 (Android 4.0.3; Linux; Opera Mobi/ADR-1210241554) Presto/2.11.355 Version/12.10",
              "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
              "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
              "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; 360SE)",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
              "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13"]

    agents_probability_list = [1, 1, 1, 2, 3, 3, 4, 4, 4, 4, 3, 2, 20, 5, 5]

    def random_agents(self):
        agent_index = self.choose_random(self.agents_probability_list)
        print(agent_index)
        return self.agents[agent_index]

    def choose_random(self, probability_list):
        """按概率选择"""
        total = 0
        for i in range(len(probability_list)):
            total += probability_list[i]

        no = random.randint(0, total)
        for i in range(len(probability_list)):
            if(no < probability_list[i]):
                return i

        return len(probability_list) - 1

    def proxy_request(self, url, agent, cookie):
        print("<proxy_request> url: " + url + "agent: " + agent)
        header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Encoding": "utf-8",
                  "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                  "Connection": "keep-alive",
                  "User-Agent": agent}

        # proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
        # opener = urllib.request.build_opener(proxy)
        # urllib.request.install_opener(opener)
        # cookie = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, headers=header)
        rsp = opener.open(req)
        print(rsp.read().decode('utf-8'))
        cookies = {}
        for item in cookie:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
            cookies.setdefault(item.name, item.value)
            return

        print(cookies)

        # response = urllib.request.urlopen(req)
        # content = response.read()
        # print(content.decode('utf8'))

    def search(self, domain, keyword, pn):
        """获取百度搜索结果"""
        search_results = []
        p = {'wd': keyword}
        header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "Accept-Encoding": "utf-8",
                  "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                  "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
        data = urllib.parse.urlencode(p)
        print(data)
        url = "http://www.baidu.com/s?" + data + "&pn={0}&cl=3&rn=100".format(pn)
        print(url)

        cookie = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, headers=header)
        response = opener.open(req)
        # print(response.read().decode('utf-8'))
        cookies = {}
        for item in cookie:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
            cookies.setdefault(item.name, item.value)

        print(cookies)

        # response = urllib.request.urlopen(req)
        content = response.read()
        # print(content.decode('utf8'))

        soup = BeautifulSoup(content.decode('utf8'))
        results = soup.find_all(attrs={'class': 'result c-container '})
        rank = 0
        for c in results:
            # print(c)
            a = c.find("a", attrs={'class': ''})
            title = a.get_text()
            print(title)
            ds = c.find("div", attrs={'class': 'c-abstract'})
            description = ds.get_text()
            print(description)
            a = c.find("a", attrs={'class': 'c-showurl'})
            display_url = a.get_text()
            print(display_url)
            target_url = a.attrs['href']
            print(target_url)
            rank += 1
            if domain in display_url:
                driver = webdriver.PhantomJS(executable_path="D:\\soft\\phantomjs\\bin\\phantomjs.exe")
                driver.get(target_url)
                driver.add_cookie(cookies)

                print("=====================page======================")
                time.sleep(3)
                print(driver.page_source)
                driver.close()
                return
            # webbrowser.open_new_tab(target_url)
            search_results.append({'rank': rank, 'title': title,
                                   'description': description,
                                   'display_url': display_url,
                                   'target_url': target_url})
            print("===========================================================")

        return search_results

    def get_rank(self, domain, keyword):
        page = 0
        results = self.search(keyword, page)
        for r in results:
            url = r['display_url']
            if domain in url:
                return {'page': page, 'rank': r['rank']}
        page = 1
        results = self.search(keyword, page)
        for r in results:
            url = r['display_url']
            if domain in url:
                return {'page': page, 'rank': r['rank']}
        page = 2
        results = self.search(keyword, page)
        for r in results:
            url = r['display_url']
            if domain in url:
                return {'page': page, 'rank': r['rank']}

        return {'page': 0, 'rank': 0}

    def start(self):
        cj = http.cookiejar.CookieJar()
        for n in range(10):
            user_agent = self.random_agents()
            time = 100 * random.randint(0, 10)
            timer = threading.Timer(time, webbrowser.open_new_tab("http://chinadmo.com/"))
            # timer = threading.Timer(time, self.proxy_request("http://chinadmo.com/", user_agent, cj))
            timer.start()

robot = SearchVisitsRobot()
# robot.start()

# for n in range(10):
#     robot.random_agents()
# br.proxy_request("http://www.chinadmo.com")
result = robot.search("www.chinadmo.com", "晶纯数字化营销", 0)
# result = robot.search("主数据管理", 1)
# result = robot.search("主数据管理", 2)
