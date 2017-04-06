#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
# from bs4 import
import xlrd
import xlwt
from src.keyword.pagekeywordstat import PageKeywordStat

class SeoSpider():

    # 已分析完的页面URL
    analyzed_urls = []

    def read_excel(self, file, sheet_name):
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_name(sheet_name)
        urls = []
        cols_count = sheet.ncols
        rows_count = sheet.nrows
        for i in range(1, rows_count):
            # row_data = []
            # for j in range(0, cols_count):
            #     row_data[j] = sheet.cell(i, j).value
            url = sheet.cell(i, 8).value
            urls.append(url)
            # print(url)
            # protocol, rest = urllib.parse.splittype(url)
            # print(rest)
            # domain, rest = urllib.parse.splithost(rest)
            # print(rest)
            # print(protocol)
            # print(domain)
        return urls

     # 输出excel
    def write_excel(self, file, sheet_name, titles, datas):
        print("<write_excel> file: " + file)
        # 创建工作簿
        wb = xlwt.Workbook()

        # 创建sheet
        sheet = wb.add_sheet(sheet_name, cell_overwrite_ok=True)

        # 初始化Title样式
        title_style = xlwt.XFStyle()
        title_font = xlwt.Font()
        #title_font.name = 'Times New Roman'
        title_font.bold = True
        title_font.color_index = 4
        title_font.height = 220

        # title_borders= xlwt.Borders()
        # title_borders.left= 6
        # title_borders.right= 6
        # title_borders.top= 6
        # title_borders.bottom= 6

        title_style.font = title_font
        # style.borders = borders

        # 初始化Cell样式
        cell_style = xlwt.XFStyle()
        cell_font = xlwt.Font()
        #cell_font.name = 'Times New Roman'
        cell_font.bold = False
        cell_font.color_index = 4
        cell_font.height = 200
        cell_style.font = cell_font

        # 生成标题行
        for i in range(0, len(titles)):
            sheet.write(0, i, titles[i], title_style)

        # 生成数据Cell
        for i in range(0, len(datas)):
            data = datas[i]
            for j in range(0, len(titles)):
                sheet.write(i + 1, j, data[j], cell_style)

        wb.save(file)

    def analyse(self, domain, url, params, keywords):
        """分析页面"""
        result = {'page_title': '', 'meta_keywords': '', 'meta_description': '', 'match_keywords': [], 'keywords': []}
        try:
            header = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                 "Accept": "text/plain"}
            data = urllib.parse.urlencode(params).encode(encoding='UTF8')
            req = urllib.request.Request(url, data, headers=header)
            response = urllib.request.urlopen(req)
            content = response.read()

            soup = BeautifulSoup(content.decode('utf8'))
            result['page_title'] = soup.title.string

            # 分析meta标签获取页面keywords和description
            meta_list = soup.find_all('meta')
            for tag in meta_list:
                if 'name' in tag.attrs:
                    if tag.attrs['name'] == "keywords":
                        result['meta_keywords'] = tag.attrs['content']
                    elif tag.attrs['name'] == "description":
                        result['meta_description'] = tag.attrs['content']

            # 分析链接
            urls = []
            u_protocol, rest = urllib.parse.splittype(url)
            u_domain, rest = urllib.parse.splithost(rest)

            link_list = soup.find_all('a')
            for tag in link_list:
                # print(tag.get_text())
                if 'href' in tag.attrs:
                    link = tag.attrs['href']
                    # print("href=" + link)
                    if link:
                        sp_url, sp_query = urllib.parse.splitquery(link)
                        # 相对路径URL补全协议和domain
                        if str(sp_url).startswith("//"):
                            sp_url = u_protocol + ":" + sp_url
                        elif str(sp_url).startswith("/"):
                            sp_url = u_protocol + "://" + u_domain + sp_url

                        if sp_url != url and domain in sp_url and sp_url not in urls:
                            urls.append(sp_url)
                        # domain, rest = urllib.parse.splithost(rest)

            urls.sort()
            print(urls)

            # 统计关键词
            page_text = soup.find("body").get_text()
            page_keyword_stat = PageKeywordStat()
            page_keyword_stat.stat_keywords(url, page_text, keywords)
            # print(page_text)
            # lines = page_text.splitlines()
            # for line in lines:
            #     if '' != line.strip():
            #         print("line=" + line.strip())
        except Exception as e:
            print(e)
        return result

    # 分析页面
    def analyse_excel_pages(self, url_excel, out_excel, sheet_name):
        urls = self.read_excel(url_excel, sheet_name)
        titles = [u'序号', u'URL', u'Page Title', u'Meta Keywords', u'Meta Description', u'关键词', u'链接数量']
        data_list = []
        for i in range(0, len(urls)):
            url = urls[i]
            print(url)
            protocol, rest = urllib.parse.splittype(url)
            domain, rest = urllib.parse.splithost(rest)
            result = self.analyse(domain, url, {}, [])
            data = []
            data.insert(0, i)
            data.insert(1, url)
            data.insert(2, result['page_title'])
            data.insert(3, result['meta_keywords'])
            data.insert(4, result['meta_description'])
            data.insert(5, '')
            data.insert(6, '')
            data_list.append(data)

        self.write_excel(out_excel, sheet_name, titles, data_list)

    # 分析页面关键词
    def analyse_pages_keywords(self, url_excel, out_excel, sheet_name):
        print("<analyse_pages_keywords> url_excel: " + url_excel + ", sheet_name: " + sheet_name)
        wb = xlrd.open_workbook(url_excel)
        sheet = wb.sheet_by_name(sheet_name)
        url_keywords_map = {}

        rows_count = sheet.nrows
        for i in range(1, rows_count):
            keyword = sheet.cell(i, 0).value
            url = sheet.cell(i, 7).value
            if keyword and url:
                sp_url, sp_query = urllib.parse.splitquery(url.strip())
                keywords = url_keywords_map.get(sp_url)
                if keywords and type(keywords) == list:
                    if keyword not in keywords:
                        keywords.append(keyword)
                else:
                    url_keywords_map.setdefault(sp_url, [keyword])

        print(url_keywords_map)

        titles = [u'序号', u'关键词', u'页面模板', u'目标页URL',
                  u'Page Title(原)', u'Page Title(新)',
                  u'Meta Keywords(原)', u'Meta Keywords(新)',
                  u'Meta Description(原)', u'Meta Description(新)',
                  u'与页面不符关键词']
        data_list = []
        n = 0
        for url in url_keywords_map:
            print(url)
            keywords = url_keywords_map.get(url)
            protocol, rest = urllib.parse.splittype(url)
            domain, rest = urllib.parse.splithost(rest)
            result = self.analyse(domain, url, {}, keywords)
            data = []
            data.insert(0, n + 1)
            data.insert(1, '')
            data.insert(2, '')
            data.insert(3, url)
            data.insert(4, result['page_title'])
            data.insert(5, '')
            data.insert(6, result['meta_keywords'])
            data.insert(7, '')
            data.insert(8, result['meta_description'])
            data.insert(9, '')
            data.insert(10, "\n".join(keywords))
            data_list.append(data)

        self.write_excel(out_excel, sheet_name, titles, data_list)

    # 分析网站
    def analyse_website(self, domain, url, out_excel, sheet_name):
        titles = [u'序号', u'URL', u'Page Title', u'Meta Keywords', u'Meta Description', u'关键词', u'链接数量']
        data_list = []
        result = self.analyse(domain, url, {}, [])
            # data = []
            # data.insert(0, 0)
            # data.insert(1, url)
            # data.insert(2, result['title'])
            # data.insert(3, result['keywords'])
            # data.insert(4, result['description'])
            # data.insert(5, '')
            # data.insert(6, '')
            # data_list.append(data)

        self.write_excel(out_excel, sheet_name, titles, data_list)

spider = SeoSpider()
#spider.analyse_excel_pages("D:\dev\python\seo-tool\conf\IBM Landing Page.xls", 'D:\dev\python\seo-tool\conf\demo.xls', "Cloud")
spider.analyse_pages_keywords("D:\dev\python\seo-tool\conf\GCG All Keywords.xls",
                              "D:\dev\python\seo-tool\conf\Keywords_Pages_LA.xls", "LA")

# result = spider.analyse("www.ibm.com", "http://www-31.ibm.com/ibm/cn/cognitive/outthink/", {})
# # result = spider.analyse("www.ibm.com", "https://www.ibm.com/analytics/cn/zh/technology/", {})
# # result = spider.analyse("www.ibm.com", "https://www.ibm.com/cn-zh/", {})
# print("title: " + result['page_title'])
# print("keywords: " + result['meta_keywords'])
# print("description: " + result['meta_description'])

print("============OK====================")